from utils.utils_dns_packet_creator import convert_name_to_bits


class RecordTypeCNAME:
    def __init__(self, cname):
        self.cname: str = cname

    def to_bin(self, name_minder: dict, seek: int):
        return convert_name_to_bits(self.cname, name_minder, seek)
