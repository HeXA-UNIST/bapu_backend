from functools import wraps
import json
from enum import Enum

from flask_socketio import emit
from src.model import User


def auth_required(auth_manager: "AuthManager"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not auth_manager.is_authenticated:
                return {"msg": "권한이 없습니다."}, 403
            return func(*args, **kwargs)

        return wrapper

    return decorator


def auth_required_on_socketio(auth_manager: "AuthManager"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not auth_manager.is_authenticated:
                emit("error", {"msg": "권한이 없습니다."}, broadcast=False)
                return  # 권한이 없으면 함수 실행을 중단
            return func(*args, **kwargs)

        return wrapper

    return decorator


class AuthState(Enum):
    LOGOUT = 0
    OTP_VERIFY = 1
    NEED_REGISTER = 2
    LOGIN = 3


class AuthManager:
    def __init__(self, session):
        self.session = session

    def enroll_user_info(self, user: User):
        user_info_dict = user.as_dict()
        encoded_user_info = json.dumps(user_info_dict)
        self.session["user_info"] = encoded_user_info

    def update_auth_state(self, auth_state: AuthState) -> None:
        self.session["auth_state"] = auth_state.value

    def get_user_info(self) -> User | None:
        user_info = self.session.get("user_info", None)
        if user_info is None:
            return User()
        return User(**json.loads(user_info))

    def clear(self) -> None:
        self.session.clear()

    @property
    def email(self) -> str | None:
        user_info = self.get_user_info()
        if user_info is None:
            return None
        return user_info.email

    @property
    def auth_state(self):
        auth_state = self.session.get("auth_state", None)
        if auth_state is None:
            return AuthState.LOGOUT
        return AuthState(auth_state)

    @property
    def nickname(self) -> str | None:
        user_info = self.get_user_info()
        if user_info is None:
            return None
        return user_info.nickname

    @property
    def user_id(self) -> str | None:
        user_info = self.get_user_info()
        return user_info.id

    @property
    def is_authenticated(self) -> bool:
        return self.auth_state == AuthState.LOGIN
