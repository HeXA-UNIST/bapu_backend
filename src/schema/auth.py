from src.middleware import ma
from src.model import Auth, User
from src.error import InvalidEmailError, NotUnistMailError


def validate_email_form(email: str):
    if not "@" in email:
        raise InvalidEmailError


def validate_unist_email(email: str):
    if not email.endswith("@unist.ac.kr"):
        raise NotUnistMailError


class RequestVerifySchema(ma.Schema):
    class Meta:
        model = Auth
        fields = ("email",)

    email = ma.Email(required=True, validate=[validate_email_form, validate_unist_email])


class CheckVerifySchema(ma.Schema):
    class Meta:
        model = Auth
        fields = ("email", "otp")

    otp = ma.Str(required=True)


class RegisterSchema(ma.Schema):
    class Meta:
        model = User

    nickname = ma.Str(required=True)
