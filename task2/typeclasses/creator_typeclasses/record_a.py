from exceptions.creator_exception import CreatorException


class RecordTypeA:
    def __init__(self, ip_v4):
        self.ip_v4: str = ip_v4

    def to_bin(self, init_seek: int):
        seek = init_seek + 32
        if self.ip_v4:
            ans = ''
            for byte in self.ip_v4.split('.'):
                ans += bin(int(byte))[2:].zfill(8)
            return ans, seek
        raise CreatorException(f'Bad address: {self.ip_v4}')
