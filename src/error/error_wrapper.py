from flask import request
from flask_socketio import emit

from functools import wraps
from .base import BaseCustomException
from marshmallow.exceptions import ValidationError


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        lang = request.args.get("lang", "kr")
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"msg": "데이터를 검증에 실패했습니니다." if lang == "kr" else "Failed to validate data."}, 400
        except BaseCustomException as e:
            return {"msg": e.get_message(lang)}, 400

    return wrapper


def handle_exceptions_on_socketio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # lang = request.args.get("lang", "kr")
        lang = "kr"
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            emit("error", {"msg": "데이터를 검증에 실패했습니니다." if lang == "kr" else "Failed to validate data."})
        except BaseCustomException as e:
            emit("error", {"msg": e.get_message(lang)})

    return wrapper
