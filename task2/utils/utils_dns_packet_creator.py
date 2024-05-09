from exceptions.creator_exception import CreatorException
from typeclasses.creator_typeclasses.record_answer import Answer
from utils.utils import TYPE_RECORD_BITS_OFFSET, CLASS_RECORD_BITS_OFFSET, TTL_OFFSET, RD_LENGTH_OFFSET

MAPPER_INVERSE_TYPE_RECORD = {'A': 1, 'NS': 2, 'CNAME': 5, 'SOA': 6, 'PTR': 12, 'MX': 15, 'TXT': 16, 'AAAA': 28}
MAPPER_INVERSE_CLASS_RECORD = {'IN': 1, 'CS': 2, 'CH': 3, 'HS': 4}

BIN_OFFSET = 2
MAX_ID = 65535
ID_SIZE = 16
OP_CODE_SIZE = 4
Z_SIZE = 3
RCODE_SIZE = 4
QDCOUNT = ANCOUNT = NSCOUNT = ARCOUNT = 16
MAX_Z = 7
QR_AA_TC_RD_RA_VALUES = [0, 1]
OP_VALUES = [0, 1, 2]
RCODE_VALUES = [0, 1, 2, 3, 4, 5]
ZIPPED_LABEL_SIZE = 14
SIMPLE_LABEL_SIZE = 6
CH_SIZE = 8
HEADER_SIZE = 96
SIMPLE_LABEL = '00'
ZIPPED_LABEL = '11'
NAME_SPLITTER = '.'
TERMINATORS_NULL = '0' * 8
CODEC = 'utf-8'


def get_bin_section(name: str) -> str:
    bin_name = ''
    for char in name:
        bin_name += bin(ord(char))[BIN_OFFSET:].zfill(CH_SIZE)
    return bin_name


def answer_to_bits(answers: list[Answer], names_minder: {}, init_seek: int):
    ans_bits = ''
    seek = init_seek
    if answers:
        for ans in answers:
            encoded_name = convert_name_to_bits(ans.name, names_minder, seek)
            seek = encoded_name[1]

            type_bits = bin(MAPPER_INVERSE_TYPE_RECORD[ans.type_record])[BIN_OFFSET:].zfill(TYPE_RECORD_BITS_OFFSET)
            class_bits = bin(MAPPER_INVERSE_CLASS_RECORD[ans.class_record])[BIN_OFFSET:].zfill(
                CLASS_RECORD_BITS_OFFSET)

            ans_bits += encoded_name[0] + type_bits + class_bits

            seek += len(type_bits) + len(class_bits)

            if ans.ttl > 2 ** 32 - 1:
                raise CreatorException(f'TTL can\'t be greater than max value({2 ** 32 - 1}):{ans.ttl}')

            ttl_bits = bin(ans.ttl)[2:].zfill(TTL_OFFSET)

            ans_bits += ttl_bits
            seek += TTL_OFFSET + RD_LENGTH_OFFSET

            rd_data = ''

            match ans.type_record:
                case 'A':
                    encoded_rd_data = ans.rdata.to_bin(seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]
                case 'AAAA':
                    encoded_rd_data = ans.rdata.to_bin(seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]
                case 'CNAME':
                    encoded_rd_data = ans.rdata.to_bin(names_minder, seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]
                case 'MX':
                    encoded_rd_data = ans.rdata.to_bin(names_minder, seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]
                case 'NS':
                    encoded_rd_data = ans.rdata.to_bin(names_minder, seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]
                case 'PTR':
                    encoded_rd_data = ans.rdata.to_bin(names_minder, seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]
                case 'SOA':
                    encoded_rd_data = ans.rdata.to_bin(names_minder, seek)
                    rd_data = encoded_rd_data[0]
                    seek = encoded_rd_data[1]

            size_rdata_bytes = int(len(rd_data) / 8)
            rd_len_bits = bin(size_rdata_bytes)[2:].zfill(RD_LENGTH_OFFSET)
            ans_bits += rd_len_bits + rd_data
            seek += len(rd_data)

    return ans_bits, seek


def convert_name_to_bits(qname: str, names_minder: dict, init_seek: int) -> tuple[str, int]:
    seek = init_seek
    query_bits = ""

    if qname in names_minder:
        label = ZIPPED_LABEL
        pointer = bin(names_minder[qname])[BIN_OFFSET:].zfill(ZIPPED_LABEL_SIZE)
        seek += len(label) + len(pointer)
        query_bits += label + pointer
    else:
        names_minder[qname] = int(seek / 8)
        for section in qname.split(NAME_SPLITTER):
            label = SIMPLE_LABEL
            size_name = bin(len(section))[BIN_OFFSET:].zfill(SIMPLE_LABEL_SIZE)
            encoded_name = get_bin_section(section)
            query_bits += label + size_name + encoded_name
            seek += len(size_name) + len(label) + len(encoded_name)

        query_bits += TERMINATORS_NULL
        seek += len(TERMINATORS_NULL)

    return query_bits, seek
