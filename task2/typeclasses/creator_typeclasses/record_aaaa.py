from exceptions.creator_exception import CreatorException


class RecordTypeAAAA:
    def __init__(self, ip_v6):
        self.ip_v6: str = ip_v6

    def to_bin(self, init_seek: int):
        seek = init_seek + 128
        if self.ip_v6:
            ans = ''
            for byte in self.ip_v6.split(':'):
                ans += bin(int(byte, 16))[2:].zfill(16)
            return ans, seek
        raise CreatorException(f'Bad address: {self.ip_v6}')
