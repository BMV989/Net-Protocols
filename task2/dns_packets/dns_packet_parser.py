from typeclasses.parser_typeclasses.record_answer import Answer
from typeclasses.parser_typeclasses.record_query import Query
from utils.utils import convert_to_bin, convert_to_read, START_ID, END_ID, START_END_QR, START_OPCODE, \
    END_OPCODE, START_END_AA, START_END_TC, START_END_RD, START_END_RA, START_RESERVED_BITS, END_RESERVED_BITS, \
    START_RCODE, END_RCODE, START_QDCOUNT, END_QDCOUNT, START_ANCOUNT, END_ANCOUNT, START_NSCOUNT, END_NSCOUNT, \
    END_ARCOUNT, START_ARCOUNT, HEADER_SIZE, parse_query, QNAME, TYPE_RECORD, CLASS_RECORD, SEEK
from utils.utils_answer import parse_answer


class DNSParser:
    def __init__(self, bytes_stream: bytes):
        bytes_for_header = convert_to_bin(bytes_stream)
        self._id = convert_to_read((bytes_for_header[START_ID: END_ID]))  # ID запроса и ID ответа совпадают
        self._QR = convert_to_read(bytes_for_header[START_END_QR])  # Запроса или ответа
        self._op_code = convert_to_read(bytes_for_header[START_OPCODE:END_OPCODE])  # Тип запроса
        self._AA = convert_to_read(bytes_for_header[START_END_AA])  # Авторитетность
        self._TC = convert_to_read(bytes_for_header[START_END_TC])  # Обрезан
        self._RD = convert_to_read(bytes_for_header[START_END_RD])  # Не сообщать промежуточных запросов
        self._RA = convert_to_read(bytes_for_header[START_END_RA])  # Поддержка рекурсии сервером
        self._Z = convert_to_read(bytes_for_header[START_RESERVED_BITS: END_RESERVED_BITS])  # Резервные биты
        self._RCODE = convert_to_read(bytes_for_header[START_RCODE: END_RCODE])  # Код состояния запроса
        self._QDCOUNT = convert_to_read(
            bytes_for_header[START_QDCOUNT: END_QDCOUNT])  # Количество записей в секции запросов
        self._ANCOUNT = convert_to_read(
            bytes_for_header[START_ANCOUNT: END_ANCOUNT])  # Количество записей в секции ответов
        self._NSCOUNT = convert_to_read(
            bytes_for_header[START_NSCOUNT: END_NSCOUNT])  # Количество записей в секции авторитета
        self._ARCOUNT = convert_to_read(
            bytes_for_header[START_ARCOUNT: END_ARCOUNT])  # Количество записей в секции дополнительно

        self._Queries = []

        seek = HEADER_SIZE

        while len(self._Queries) < self._QDCOUNT:
            parsed_query = parse_query(bytes_for_header, seek)
            query = Query(parsed_query[QNAME], parsed_query[TYPE_RECORD], parsed_query[CLASS_RECORD])
            self._Queries.append(query)
            seek = parsed_query[SEEK]

        parsed_answer = parse_answer(bytes_for_header, [], self._ANCOUNT, seek)

        self._Answers = parsed_answer[0]
        seek = parsed_answer[1]

        parsed_authority = parse_answer(bytes_for_header, [], self._NSCOUNT, seek)

        self._Authority = parsed_authority[0]
        seek = parsed_authority[1]

        parsed_additional = parse_answer(bytes_for_header, [], self._ARCOUNT, seek)

        self._Additional = parsed_additional[0]

    @property
    def id(self) -> int:
        return self._id

    @property
    def qr(self) -> int:
        return self._QR

    @property
    def op_code(self) -> int:
        return self._op_code

    @property
    def aa(self) -> int:
        return self._AA

    @property
    def tc(self) -> int:
        return self._TC

    @property
    def rd(self) -> int:
        return self._RD

    @property
    def ra(self) -> int:
        return self._RA

    @property
    def z(self) -> int:
        return self._Z

    @property
    def rcode(self) -> int:
        return self._RCODE

    @property
    def qdcount(self) -> int:
        return self._QDCOUNT

    @property
    def ancount(self) -> int:
        return self._ANCOUNT

    @property
    def nscount(self) -> int:
        return self._NSCOUNT

    @property
    def arcount(self) -> int:
        return self._ARCOUNT

    @property
    def queries_list(self) -> list[Query]:
        return self._Queries

    @property
    def answers_list(self) -> list[Answer]:
        return self._Answers

    @property
    def authority_list(self) -> list[Answer]:
        return self._Authority

    @property
    def additional_list(self) -> list[Answer]:
        return self._Additional
