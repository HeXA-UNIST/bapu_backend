from flask import Blueprint, request, session

from src.schema import RequestVerifySchema, RegisterSchema, CheckVerifySchema
from src.error import handle_exceptions
from src.utils import OTPManager, AuthManager, send_mail, AuthState, auth_required
from src.model import Auth, User

auth_router = Blueprint("auth", __name__)
request_verify_schema = RequestVerifySchema()
check_verify_schema = CheckVerifySchema()
register_schema = RegisterSchema()
otp_manager = OTPManager()
auth_manager = AuthManager(session)


# 인증번호 요청
@auth_router.route("/request_verify", methods=["POST"])
@handle_exceptions
def request_verify():
    # 올바른 형식인지 확인
    req_data = request.get_json()
    request_verify_schema.validate(req_data)
    req_data = request_verify_schema.load(req_data)

    # 인증코드 만들어서 전송
    otp_code = otp_manager.create_safe_random_otp_code()
    auth = Auth().create(email=req_data.get("email"), otp=otp_code)
    send_mail(auth.email, "TaxiHeXA 인증번호", f"Your OTP code is: {otp_code}. It is valid for 5 minutes.")

    # 가상 유저 인스턴스 생성 후 session 에 등록
    email_user = User(
        email=req_data.get("email"),
    )
    auth_manager.enroll_user_info(email_user)
    # auth state 변경
    auth_manager.update_auth_state(AuthState.OTP_VERIFY)
    return {"msg": "OTP sent successfully."}, 200


# 인증번호 확인
@auth_router.route("/check_verify", methods=["POST"])
@handle_exceptions
def check_verify():
    # 올바른 형식인지 확인
    req_data = request.get_json()
    check_verify_schema.validate(req_data)
    req_data = check_verify_schema.load(req_data)

    if auth_manager.auth_state != AuthState.OTP_VERIFY:
        return {"msg": "email정보가 존재하지 않습니다."}, 401

    req_otp_code = req_data.get("otp")
    req_email = auth_manager.email
    otp_manager.verified_otp(otp_code=req_otp_code, email=req_email)

    user = User.select_by_email(req_email)
    if user and user.is_banned:
        return {"msg": "You are banned."}, 403

    if user:
        auth_manager.enroll_user_info(user)
        auth_manager.update_auth_state(AuthState.LOGIN)
    else:
        auth_manager.update_auth_state(AuthState.NEED_REGISTER)

    return {
        "msg": "Check success.",
        "registered": auth_manager.auth_state == AuthState.LOGIN,
        "nickname": auth_manager.nickname,
    }, 200


@auth_router.route("/logout", methods=["POST"])
@handle_exceptions
def logout():
    auth_manager.clear()
    return {"msg": "Logout success."}, 200


@auth_router.route("/profile", methods=["GET"])
@handle_exceptions
@auth_required(auth_manager)
def get_profile():
    print(session.items())
    return auth_manager.get_user_info().as_dict(), 200


@auth_router.route("/register", methods=["POST"])
@handle_exceptions
def register_user():
    req_data = request.get_json()
    register_schema.validate(req_data)

    if not auth_manager.auth_state == AuthState.NEED_REGISTER:
        return {"msg": "로그인 상태가 일치하지 않습니다."}, 401

    duplicated_user_by_nickname = User.select_by_nickname(req_data.get("nickname"))
    if duplicated_user_by_nickname:
        return {"msg": "중복된 닉네임입니다."}, 401

    user = User().create(email=auth_manager.email, nickname=req_data.get("nickname"))
    auth_manager.clear()
    auth_manager.enroll_user_info(user)
    auth_manager.update_auth_state(AuthState.LOGIN)

    return {"msg": "User registered successfully."}, 200
