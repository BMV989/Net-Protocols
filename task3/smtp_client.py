import json
import re
import os
import logging
from dotenv import load_dotenv
import ssl
import socket
import magic
import base64
from random import randint

RE_RUSSIAN_SUBJECT = re.compile(r'[а-яА-ЯёЁ]')
RE_DOT_OR_DOTS = re.compile(r'^\.+$')

load_dotenv()

MAIL = os.getenv('MAIL')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
HOST_ADDRESS = os.getenv('HOST_ADDRESS')
PORT = int(os.getenv('PORT'))

logging.basicConfig(level=logging.INFO)


def normalize_subject(subject: str) -> str:
    if subject and not RE_RUSSIAN_SUBJECT.search(subject):
        return f"Subject: {subject}\n"

    parts = []
    for i in range(0, len(subject), 30):
        part = subject[i:min(len(subject), i + 30)]
        base64part = base64.b64encode(part.encode()).decode()
        parts.append(f'=?utf-8?B?{base64part}?=')
    return f"Subject: {'\n\t'.join(parts)}\n"


def send_request(client: socket.socket, request: str) -> str:
    client.send((request + '\n').encode())
    return socket.recv(1024).decode()


def generate_boundary() -> str:
    return f"bound.{''.join([chr(randint(97, 123)) for _ in range(10)])}"


def parse_json_mail() -> dict | None:
    try:
        with open(MAIL, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(e)
        return None


def build_message(mail: dict | None) -> str | None:
    try:
        message_parts = []
        boundary = generate_boundary()

        message_parts.append(f'From: <{LOGIN}@yandex.ru>\n')
        message_parts.append(f'To: ' + ',\n\t'.join(map(lambda s: f'<{s}>', mail["receivers"])) + '\n')
        message_parts.append(normalize_subject(mail['subject']))
        message_parts.append('MIME-Version: 1.0\n')
        message_parts.append(f"Content-Type: multipart/mixed;boundary=\"{boundary}\"\n\n\n")

        message_parts.append(f"--{boundary}\n")
        message_parts.append("Content-Type: text/html\n\n")
        for line in mail["body"].split("\n"):
            if RE_DOT_OR_DOTS.match(line):
                line += "."
            message_parts.append(f"{line}\n")

        for attach in mail["attachments"]:
            filename = os.path.split(attach)[1]
            try:
                with open(attach, "rb") as file:
                    message_parts.append(f"--{boundary}\n")
                    message_parts.append("Content-Disposition: attachment;\n")
                    message_parts.append(f"\tfilename=\"{filename}\"\n")
                    message_parts.append("Content-Transfer-Encoding: base64\n")
                    mime_type = magic.from_file(attach, mime=True)
                    message_parts.append(f"Content-Type: {mime_type};\n")
                    message_parts.append(f"\tname=\"{filename}\"\n\n")
                    content = base64.b64encode(file.read()).decode("utf-8")
                    message_parts.append(content + '\n')
                    message_parts.append(f"--{boundary}--")
                    message_parts.append("\n.\n")
            except Exception as e:
                logging.error(f"can't add your {attach} because of an error: {e}")
                continue
        return ''.join(message_parts)
    except Exception as e:
        logging.error(e)
        return None


def send_mail(mail: dict | None) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST_ADDRESS, PORT))
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            client = context.wrap_socket(client)

            client.recv(1024)
            send_request(client, f"EHLO {LOGIN}")
            base64login = base64.b64encode(login.encode()).decode()
            base64password = base64.b64encode(password.encode()).decode()
            send_request(client, base64login)
            response = send_request(client, base64password)
            if not response.startswith("235"):
                raise ConnectionError
            response = send_request(client, f'MAIL FROM:{LOGIN}@yandex.ru')
            if not response.startswith("250"):
                raise ValueError(LOGIN)
            for receiver in mail["receivers"]:
                response = send_request(client, f"RCPT TO:{receiver}")
                if not response.startswith("250"):
                    raise Exception(f"wrong receiver: {receiver}")
            send_request(client, 'DATA')
            send_request(client, build_message(mail))
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    send_mail(parse_json_mail())
