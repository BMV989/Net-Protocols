class RecordTypeAAAA:
    def __init__(self, bits_stream: str):
        octets = []
        for i in range(0, len(bits_stream), 16):
            octet = hex(int(bits_stream[i: i + 16], 2))[2:]
            octets.append(octet)
        self._ip_v6 = ':'.join(octets)

    @property
    def ip(self):
        return self._ip_v6