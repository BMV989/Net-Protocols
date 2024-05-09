from utils.utils import parse_names

SERIAL_NUMBER_OFFSET = 32
REFRESH_INTERVAL_OFFSET = 32
RETRY_INTERVAL_OFFSET = 32
EXPIRE_LIMIT_OFFSET = 32
MINIMUM_TTL_OFFSET = 32


class RecordTypeSoa:
    def __init__(self, bits_stream: str, start_soa_seek: int):
        parsed_primary_server = parse_names(bits_stream, start_soa_seek)
        self._primary_server = parsed_primary_server[0]
        parsed_authority_server = parse_names(bits_stream, parsed_primary_server[1])
        self._responsible_authority = parsed_authority_server[0]

        seek = parsed_authority_server[1]
        self._serial_number = int(bits_stream[seek: seek + SERIAL_NUMBER_OFFSET], 2)
        seek += SERIAL_NUMBER_OFFSET
        self._refresh_interval = int(bits_stream[seek: seek + REFRESH_INTERVAL_OFFSET], 2)
        seek += REFRESH_INTERVAL_OFFSET
        self._retry_interval = int(bits_stream[seek: seek + RETRY_INTERVAL_OFFSET], 2)
        seek += RETRY_INTERVAL_OFFSET
        self._expire_limit = int(bits_stream[seek: seek + EXPIRE_LIMIT_OFFSET], 2)
        seek += EXPIRE_LIMIT_OFFSET
        self._minimum_ttl = int(bits_stream[seek: seek + MINIMUM_TTL_OFFSET], 2)
        seek += MINIMUM_TTL_OFFSET

    @property
    def primary_server(self):
        return self._primary_server

    @property
    def responsible_authority(self):
        return self._responsible_authority

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def refresh_interval(self):
        return self._refresh_interval

    @property
    def retry_interval(self):
        return self._retry_interval

    @property
    def expire_limit(self):
        return self._expire_limit

    @property
    def minimum_ttl(self):
        return self._minimum_ttl
