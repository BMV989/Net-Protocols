from utils.utils_dns_packet_creator import convert_name_to_bits
from exceptions.creator_exception import CreatorException


class RecordTypeNS:
    def __init__(self, authority_name_server):
        self.authority_name_server = authority_name_server

    def to_bin(self, names_minder: dict, start_ns_seek: int):
        if self.authority_name_server:
            encoded_name = convert_name_to_bits(self.authority_name_server, names_minder, start_ns_seek)
            seek = encoded_name[1]
            return encoded_name[0], seek
        raise CreatorException(f'Invalid authority server: {self.authority_name_server}')
