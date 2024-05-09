from exceptions.creator_exception import CreatorException
from utils.utils_dns_packet_creator import convert_name_to_bits

PREFERENCE_OFFSET = 16


class RecordTypeMX:
    def __init__(self, preference, mail_exchange):
        self.preference = preference
        self.mail_exchange = mail_exchange

    def to_bin(self, names_minder: dict, start_mx_seek: int):
        if self.preference and self.mail_exchange:
            bits_preferences = bin(self.preference)[2:].zfill(PREFERENCE_OFFSET)
            encoded_mail_exchange = convert_name_to_bits(self.mail_exchange, names_minder, start_mx_seek + PREFERENCE_OFFSET)
            seek = encoded_mail_exchange[1]
            bits_mail_exchange = encoded_mail_exchange[0]
            return bits_preferences + bits_mail_exchange, seek
        raise CreatorException(f'Invalid params: preference: {self.preference}, mail exchange: '
                               f'{self.mail_exchange}')
