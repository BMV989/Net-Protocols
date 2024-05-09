class Answer:
    def __init__(self, name: str, type_record: str, class_record: str, ttl_sec: int, rd_length: int, rdata):
        self._Name = name
        self._Type_record = type_record
        self._Class_record = class_record
        self._TTL_sec = ttl_sec
        self._RD_length = rd_length
        self._Rdata = rdata


    @property
    def name(self) -> str:
        return self._Name

    @property
    def type_record(self) -> str:
        return self._Type_record

    @property
    def class_record(self) -> str:
        return self._Class_record

    @property
    def ttl(self) -> int:
        return self._TTL_sec

    @property
    def rd_len(self) -> int:
        return self._RD_length

    @property
    def rdata(self):
        return self._Rdata
