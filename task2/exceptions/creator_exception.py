class CreatorException(Exception):
    def __init__(self, text: str):
        self.info = text

    @property
    def text(self):
        return self.info
