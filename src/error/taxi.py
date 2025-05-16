from .base import BaseCustomException


class InvalidTimeError(BaseCustomException):
    def __init__(self):
        super().__init__("유효하지 않은 시간입니다.", "Invalid time.")
