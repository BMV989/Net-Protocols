from utils.utils_dns_packet_creator import convert_name_to_bits
from exceptions.creator_exception import CreatorException


class RecordTypePTR:
    def __init__(self, name: str):
        self.name: str = name

    def to_bin(self, names_minder: dict, start_ptr_seek: int):
        if self.name:
            encoded_name = convert_name_to_bits(self.name, names_minder, start_ptr_seek)
            return encoded_name[0], encoded_name[1]
        raise CreatorException(f'Bad PTR: {self.name}')
