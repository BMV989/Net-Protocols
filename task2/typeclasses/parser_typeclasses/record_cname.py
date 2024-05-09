from utils.utils import parse_names


class RecordTypeCNAME:
    def __init__(self, bits_stream: str, start_cname_seek: int):
        self._cname = parse_names(bits_stream, start_cname_seek)[0]

    @property
    def cname(self):
        return self._cname