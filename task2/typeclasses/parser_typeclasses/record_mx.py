from utils.utils import parse_names

PREFERENCE_OFFSET = 16


class RecordTypeMX:
    def __init__(self, bits_stream: str, start_mx_seek: int):
        self._preference = int(bits_stream[start_mx_seek: start_mx_seek + PREFERENCE_OFFSET], 2)
        seek = start_mx_seek + PREFERENCE_OFFSET
        self._mail_exchange = parse_names(bits_stream, seek)[0]

    @property
    def preference(self):
        return self._preference

    @property
    def mail_exchange(self):
        return self._mail_exchange
