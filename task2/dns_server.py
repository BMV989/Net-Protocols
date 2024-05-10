from dotenv import load_dotenv
import json
import time
import logging
import os
import socket
import binascii
from typeclasses.creator_typeclasses.record_a import RecordTypeA
from typeclasses.creator_typeclasses.record_aaaa import RecordTypeAAAA
from typeclasses.creator_typeclasses.record_cname import RecordTypeCNAME
from typeclasses.creator_typeclasses.record_mx import RecordTypeMX
from typeclasses.creator_typeclasses.record_ns import RecordTypeNS
from typeclasses.creator_typeclasses.record_ptr import RecordTypePTR
from typeclasses.creator_typeclasses.record_soa import RecordTypeSoa
from dns_packets.config_dns import DNSConfig
from dns_packets.dns_packet_creator import DNSCreator
from dns_packets.dns_packet_parser import DNSParser
from typeclasses.creator_typeclasses.record_answer import Answer
from utils.utils_server import resolve_name
from utils.utils_dns_config import to_creator


class Cache:
    def __init__(self):
        self.__cache = {}

    def clear(self):
        self.__cache.clear()

    def put(self, name: str, type_record: str, rdata, ttl):
        self.__cache[f'{name}|{type_record}'] = (rdata, ttl, int(time.time()))

    def get(self, name: str, type_record: str):
        timer = int(time.time())

        for key, values in self.__cache.copy().items():
            if abs(timer - values[2]) > values[1]:
                self.__cache.pop(key)

        return self.__cache.get(f'{name}|{type_record}')

    def from_json(self, filename: str):
        with open(filename, 'a+') as f:
            try:
                data: dict = json.load(f)
                for key, value in data.items():
                    record_type = key.split('|')[-1]
                    val = ''
                    match record_type:
                        case 'A':
                            val = (RecordTypeA(value[0]['ip_v4']), value[1], value[2])
                        case 'AAAA':
                            val = (RecordTypeAAAA(value[0]['ip_v6']), value[1], value[2])
                        case 'CNAME':
                            val = (RecordTypeCNAME(value[0]['cname']), value[1], value[2])
                        case 'MX':
                            val = (RecordTypeMX(value[0]['preference'], value[0]['mail_exchange']), value[1], value[2])
                        case 'NS':
                            val = (RecordTypeNS(value[0]['authority_name_server']), value[1], value[2])
                        case 'PTR':
                            val = (RecordTypePTR(value[0]['name']), value[1], value[2])
                        case 'SOA':
                            fields = value[0]
                            val = (RecordTypeSoa(fields['primary_server'], fields['responsible_authority'],
                                                 fields['serial_number'], fields['refresh_interval'],
                                                 fields['retry_interval'], fields['expire_limit'],
                                                 fields['minimum_ttl']), value[1], value[2])

                    self.__cache[key] = val
            except json.JSONDecodeError:
                return None

    def to_json(self, filename: str):
        with open(filename, 'w') as file:
            data = self.__cache
            json.dump(data, file, default=lambda x: x.__dict__)


load_dotenv()

PORT = int(os.getenv('PORT')) or 53
FORWARDER = os.getenv('FORWARDER') or '8.8.8.8'
CACHE = os.getenv('CACHE') or 'cache.json'

logging.basicConfig(level=logging.INFO, filename='dns_server.log', filemode='a')


def resolution_loop(server: socket.socket, forwarder: str, cache: Cache):
    while True:
        try:
            data, addr = server.recvfrom(1024)
            logging.info(f'{addr} connected')

            hex_data = binascii.b2a_hex(data)
            logging.info(f'read from {addr} : {hex_data}')
            query_packet = DNSParser(hex_data)
            std_dns_config = DNSConfig().from_parsed_packet(query_packet)
            std_dns_config.QR = 1

            for query in query_packet.queries_list:
                answer = cache.get(query.qname, query.type_record)

                if not answer:
                    answer_query = resolve_name(query.qname, query.type_record, query.class_record, forwarder)
                    logging.info(f'{query.qname} : {query.type_record} was resolved from forwarder')

                    for resolved_answer in answer_query.answers_list:
                        rdata = to_creator(resolved_answer)
                        cache.put(resolved_answer.name, resolved_answer.type_record, rdata, resolved_answer.ttl)
                        std_dns_config.ANSWERS.append(Answer(resolved_answer.name, resolved_answer.type_record, resolved_answer.class_record, resolved_answer.ttl, rdata))
                else:
                    logging.info(f'{query.qname}|{query.type_record} was got from cache')
                    std_dns_config.ANSWERS.append(
                        Answer(query.qname, query.type_record, query.class_record, answer[1], answer[0]))

            answer_dns = DNSCreator(std_dns_config).to_bin()

            if len(answer_dns) % 2:
                answer_dns = '0' + answer_dns

            server.sendto(bytes.fromhex(answer_dns), addr)

        except KeyboardInterrupt:
            logging.info('ctrl+c received, shutting down')
            cache.to_json(CACHE)
            break
        except OSError:
            logging.error("Network is unreachable")
        except Exception as err:
            logging.error(err)
            continue


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            cache = Cache()
            cache.from_json(CACHE)
            server.bind(('127.0.0.1', PORT))
            logging.info(f'DNS server is running at 127.0.0.1:{PORT}, press ctr+c to stop it')
            resolution_loop(server, FORWARDER, cache)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()
