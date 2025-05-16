from .base import BaseCustomException


class InvalidEmailError(BaseCustomException):
    def __init__(self):
        super().__init__("유효하지 않은 이메일입니다.", "Invalid email.")


class NotUnistMailError(BaseCustomException):
    def __init__(self):
        super().__init__("유니스트 이메일이 아닙니다.", "Not UNIST email.")


class EmailNotFoundError(BaseCustomException):
    def __init__(self):
        super().__init__("이메일을 찾을 수 없습니다.", "Email not found.")


class OTPCodeIsNotSameError(BaseCustomException):
    def __init__(self):
        super().__init__("인증 코드가 일치하지 않습니다.", "Auth code is not same.")


class OTPExpiredError(BaseCustomException):
    def __init__(self):
        super().__init__("인증 코드가 만료되었습니다.", "Auth code is expired.")


class EmailNotFoundInOTPError(BaseCustomException):
    def __init__(self):
        super().__init__("이메일을 찾을 수 없습니다.", "Email not found in OTP.")


class MaxRetriesError(BaseCustomException):
    def __init__(self):
        super().__init__("최대 시도 횟수를 초과하였습니다.", "Max retries exceeded.")


class AlreadyVerifiedError(BaseCustomException):
    def __init__(self):
        super().__init__("이미 인증된 이메일입니다.", "Email is already verified.")
