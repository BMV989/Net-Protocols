from dns_packets.config_dns import DNSConfig
from exceptions.creator_exception import CreatorException
from utils.utils import TYPE_RECORD_BITS_OFFSET, CLASS_RECORD_BITS_OFFSET
from utils.utils_dns_packet_creator import MAX_ID, BIN_OFFSET, QR_AA_TC_RD_RA_VALUES, OP_VALUES, OP_CODE_SIZE, MAX_Z, Z_SIZE, \
    RCODE_VALUES, RCODE_SIZE, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT, HEADER_SIZE, convert_name_to_bits, \
    MAPPER_INVERSE_TYPE_RECORD, MAPPER_INVERSE_CLASS_RECORD, answer_to_bits


class DNSCreator:
    def __init__(self, config: DNSConfig):
        self._config = config

    def to_bin(self):
        bytes_packet = ''

        names_minder = self._config.names_minder

        if self._config.ID > MAX_ID:
            raise CreatorException(f"ID can\'t be greater than id (65535): {self._config.ID}")

        id_bits: str = bin(self._config.ID)[BIN_OFFSET:].zfill(16)

        bytes_packet += id_bits

        if self._config.QR not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Field can\'t be identified as query or answer (0, 1): {self._config.QR}')

        qr_bits: str = str(self._config.QR)

        bytes_packet += qr_bits

        if self._config.OP_CODE not in OP_VALUES:
            raise CreatorException(
                f'Field can\'t be identified as opcode (0, 1, 2): {self._config.OP_CODE}')

        op_code_bits: str = bin(self._config.OP_CODE)[BIN_OFFSET:].zfill(OP_CODE_SIZE)

        bytes_packet += op_code_bits

        if self._config.AA not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Field can\'t be identified as authority code (0, 1): {self._config.AA}')

        aa_bits: str = str(self._config.AA)

        bytes_packet += aa_bits

        if self._config.TC not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Field can\'t be identified as truncated (0, 1): {self._config.TC}')

        tc_bits: str = str(self._config.TC)

        bytes_packet += tc_bits

        if self._config.RD not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Field can\'t be identified as recursion desire (0, 1): {self._config.RD}')

        rd_bits: str = str(self._config.RD)

        bytes_packet += rd_bits

        if self._config.RA not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Field can\'t be identified as recursion available (0, 1): {self._config.RA}')

        ra_bits: str = str(self._config.RA)

        bytes_packet += ra_bits

        if self._config.Z > MAX_Z:
            raise CreatorException(
                f"Value in field can\'t be greater than 7 because field size is 3 bits: {self._config.Z}")

        z_bits: str = bin(self._config.Z)[BIN_OFFSET:].zfill(Z_SIZE)

        bytes_packet += z_bits

        if self._config.RCODE not in RCODE_VALUES:
            raise CreatorException(
                f"Field can\'t be identified as status of request completion (0, 1, 2, 3, 4, 5) {self._config.RCODE}")

        rcode_bits: str = bin(self._config.RCODE)[BIN_OFFSET:].zfill(RCODE_SIZE)

        bytes_packet += rcode_bits

        qdcount_bits: str = bin(len(self._config.QUERIES))[BIN_OFFSET:].zfill(QDCOUNT)
        ancount_bits: str = bin(len(self._config.ANSWERS))[BIN_OFFSET:].zfill(ANCOUNT)
        nscount_bits: str = bin(len(self._config.AUTHORITY))[BIN_OFFSET:].zfill(NSCOUNT)
        arcount_bits: str = bin(len(self._config.ADDITIONAL))[BIN_OFFSET:].zfill(ARCOUNT)

        bytes_packet += qdcount_bits + ancount_bits + nscount_bits + arcount_bits

        query_bits: str = ""

        seek = HEADER_SIZE

        for record in self._config.QUERIES:
            encoded_qname = convert_name_to_bits(record.qname, names_minder, seek)

            seek = encoded_qname[1]
            query_bits += encoded_qname[0]

            type_record_bits = bin(MAPPER_INVERSE_TYPE_RECORD[record.type_record])[BIN_OFFSET:].zfill(
                TYPE_RECORD_BITS_OFFSET)
            class_record_bits = bin(MAPPER_INVERSE_CLASS_RECORD[record.class_record])[BIN_OFFSET:].zfill(
                CLASS_RECORD_BITS_OFFSET)
            query_bits += type_record_bits + class_record_bits
            seek += len(type_record_bits) + len(class_record_bits)

        answer_bits, seek = answer_to_bits(self._config.ANSWERS, names_minder, seek)
        authority_bits, seek = answer_to_bits(self._config.AUTHORITY, names_minder, seek)
        additional_bits, seek = answer_to_bits(self._config.ADDITIONAL, names_minder, seek)

        bytes_packet += query_bits + answer_bits + authority_bits + additional_bits

        return hex(int(bytes_packet, 2))[2:]
