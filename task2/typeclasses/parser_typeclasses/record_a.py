class RecordTypeA:
    def __init__(self, bits_stream: str):
        octets = []
        for i in range(0, len(bits_stream), 8):
            octet = int(bits_stream[i: i + 8], 2)
            octets.append(str(octet))
        self._ip_v4 = '.'.join(octets)

    @property
    def ip(self) -> str:
        return self._ip_v4
