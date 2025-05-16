import secrets
from datetime import datetime, timedelta
from src.error import OTPCodeIsNotSameError, OTPExpiredError, EmailNotFoundInOTPError, MaxRetriesError, AlreadyVerifiedError

from src.model import Auth


class OTPManager:
    def create_safe_random_otp_code(self, digits: int = 6) -> str:
        otp_code = "".join(secrets.choice("0123456789") for _ in range(digits))
        return otp_code

    def verified_otp(self, otp_code: str, email: str, timeout: int = 300, max_retries: int = 4) -> None:
        auth = Auth.select_by_email(email)
        if auth is None:
            raise EmailNotFoundInOTPError
        elif auth.is_verified:
            return AlreadyVerifiedError
        elif auth.num_tries > max_retries:
            raise MaxRetriesError
        elif not otp_code == auth.otp:
            auth.update_num_tries()
            raise OTPCodeIsNotSameError
        elif auth.created_at + timedelta(seconds=timeout) < datetime.now():
            raise OTPExpiredError
        auth.update_is_verified(True)
