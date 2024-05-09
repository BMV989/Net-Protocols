from utils.utils import parse_names


class RecordTypeNS:
    def __init__(self, bits_stream: str, start_ns_seek: int):
        self._authority_name_server = parse_names(bits_stream, start_ns_seek)[0]

    @property
    def name_server(self):
        return self._authority_name_server