class Query:
    def __init__(self, name: str, type_record: str, class_record: str):
        self._QName = name
        self._Type_Record = type_record
        self._Class_Record = class_record

    @property
    def qname(self):
        return self._QName

    @property
    def type_record(self):
        return self._Type_Record

    @property
    def class_record(self):
        return self._Class_Record
