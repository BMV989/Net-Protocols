from utils.utils import parse_names


class RecordTypePTR:
    def __init__(self, bits_stream: str, start_ptr_seek: int):
        self._name = parse_names(bits_stream, start_ptr_seek)[0]

    @property
    def name_server(self):
        return self._name