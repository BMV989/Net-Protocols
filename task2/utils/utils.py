import enum

START_ID = 0
END_ID = 16

START_END_QR = 16

START_OPCODE = 17
END_OPCODE = 21

START_END_AA = 21

START_END_TC = 22
START_END_RD = 23
START_END_RA = 24

START_RESERVED_BITS = 25
END_RESERVED_BITS = 28

START_RCODE = 28
END_RCODE = 32

START_QDCOUNT = 32
END_QDCOUNT = 48

START_ANCOUNT = 48
END_ANCOUNT = 64

START_NSCOUNT = 64
END_NSCOUNT = 80

START_ARCOUNT = 80
END_ARCOUNT = 96

HEADER_SIZE = 96

HALF_BITE_SIZE = 4

INDENT_BYTES = 2

TYPE_LABEL_OFFSET = 2
LABEL_SIZE_OFFSET = 6
LABEL_OFFSET_BITS_SIZE = 14

TYPE_RECORD_BITS_OFFSET = 16
CLASS_RECORD_BITS_OFFSET = 16

TTL_OFFSET = 32
RD_LENGTH_OFFSET = 16

QNAME = 0
TYPE_RECORD = 1
CLASS_RECORD = 2
SEEK = 3

MAPPER_TYPE_RECORD = {1: 'A', 2: 'NS', 5: 'CNAME', 6: 'SOA', 12: 'PTR', 15: 'MX', 16: 'TXT', 28: 'AAAA', 255: 'ANY'}
MAPPER_CLASS_RECORD = {1: 'IN', 2: 'CS', 3: 'CH', 4: 'HS'}


class TypesLabel(enum.StrEnum):
    STD_TYPE_LABEL = '00'
    ZIPPED_TYPE_LABEL = '11'


def bin_to_name(lead: str):
    name = ""
    for i in range(0, len(lead), 8):
        char = chr(int(lead[i: i + 8], 2))
        name += char
    return name


def parse_names(bits_stream: str, init_seek: int) -> tuple[str, int]:
    seek = init_seek
    old_seek = seek
    name = []

    while True:
        type_label: str = bits_stream[seek: seek + TYPE_LABEL_OFFSET]
        seek += TYPE_LABEL_OFFSET

        match type_label:
            case TypesLabel.STD_TYPE_LABEL:
                label_size = int(bits_stream[seek: seek + LABEL_SIZE_OFFSET], 2) * 8
                seek += LABEL_SIZE_OFFSET

                if label_size == 0:
                    break

                section = bin_to_name(bits_stream[seek: seek + label_size])
                seek += label_size
                name.append(section)

            case TypesLabel.ZIPPED_TYPE_LABEL:
                seek_offset = int(bits_stream[seek: seek + LABEL_OFFSET_BITS_SIZE], 2) * 8
                old_seek = seek + LABEL_OFFSET_BITS_SIZE
                seek = seek_offset

    qname: str = '.'.join(name)

    if old_seek > seek:
        seek = old_seek

    return qname, seek


def parse_query(bits_stream: str, init_seek: int) -> tuple[str, str, str, int]:
    seek = init_seek
    old_seek = seek
    is_moved = False
    name = []

    while True:
        type_label: str = bits_stream[seek: seek + TYPE_LABEL_OFFSET]
        seek += TYPE_LABEL_OFFSET

        match type_label:
            case TypesLabel.STD_TYPE_LABEL:
                label_size = int(bits_stream[seek: seek + LABEL_SIZE_OFFSET], 2) * 8
                seek += LABEL_SIZE_OFFSET

                if label_size == 0:
                    break

                section = bin_to_name(bits_stream[seek: seek + label_size])
                seek += label_size
                name.append(section)

            case TypesLabel.ZIPPED_TYPE_LABEL:
                seek_offset = int(bits_stream[seek: seek + LABEL_OFFSET_BITS_SIZE], 2) * 8

                if not is_moved:
                    old_seek = seek + LABEL_OFFSET_BITS_SIZE
                    is_moved = True

                seek = seek_offset

    qname: str = '.'.join(name)

    if old_seek > seek:
        seek = old_seek

    type_record = MAPPER_TYPE_RECORD[int(bits_stream[seek: seek + TYPE_RECORD_BITS_OFFSET], 2)]
    seek += TYPE_RECORD_BITS_OFFSET

    class_record = MAPPER_CLASS_RECORD[int(bits_stream[seek: seek + CLASS_RECORD_BITS_OFFSET], 2)]
    seek += CLASS_RECORD_BITS_OFFSET

    return qname, type_record, class_record, seek


def to_number(lead: str) -> int:
    return int(lead, 2)


def convert_to_read(lead: str) -> int:
    return to_number(lead)


def convert_to_bin(lead: bytes) -> str:
    result = ""
    for byte in lead:
        num = int(chr(byte), 16)
        bin_num = bin(num)[INDENT_BYTES:].zfill(HALF_BITE_SIZE)
        result += bin_num
    return result
