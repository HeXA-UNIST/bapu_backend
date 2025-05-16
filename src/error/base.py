class BaseCustomException(Exception):
    def __init__(self, kr_message: str | None = None, en_message: str | None = None):
        self.message = {"kr": kr_message, "en": en_message}
        super().__init__(self.message)

    def get_message(self, lang: str = "kr") -> str:
        return self.message[lang]

    def __str__(self):
        return self.message["kr"]

    def __repr__(self):
        return self
