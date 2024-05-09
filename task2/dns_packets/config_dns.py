from __future__ import annotations

from random import randint

from dns_packets.dns_packet_parser import DNSParser
from typeclasses.parser_typeclasses.record_query import Query
from typeclasses.creator_typeclasses.record_answer import Answer
from utils.utils_dns_config import creators_from_answers


class DNSConfig:
    def __init__(self):
        self.ID = None
        self.QR = None
        self.OP_CODE = None
        self.AA = None
        self.TC = None
        self.RD = None
        self.RA = None
        self.Z = None
        self.RCODE = None
        self.QUERIES: list[Query] = []
        self.ANSWERS: list[Answer] = []
        self.AUTHORITY: list[Answer] = []
        self.ADDITIONAL: list[Answer] = []
        self.names_minder: dict = {}

    def from_parsed_packet(self, parsed_packet: DNSParser):
        self.ID = parsed_packet.id
        self.QR = parsed_packet.qr
        self.OP_CODE = parsed_packet.op_code
        self.AA = parsed_packet.aa
        self.TC = parsed_packet.tc
        self.RD = parsed_packet.rd
        self.RA = parsed_packet.ra
        self.Z = parsed_packet.z
        self.RCODE = parsed_packet.rcode
        self.QUERIES = parsed_packet.queries_list

        creators_from_answers(parsed_packet.answers_list, self.ANSWERS)
        creators_from_answers(parsed_packet.authority_list, self.AUTHORITY)
        creators_from_answers(parsed_packet.additional_list, self.ADDITIONAL)
        return self

    def set_query(self, name_or_ip: str, record_type: str, class_record: str) -> DNSConfig:
        self.ID = randint(1, 2 ** 16 - 1)
        self.QR = 0
        self.OP_CODE = 0
        self.AA = 0
        self.TC = 0
        self.RD = 1
        self.RA = 0
        self.Z = 0
        self.RCODE = 0
        self.QUERIES = [Query(name_or_ip, record_type, class_record)]
        return self
