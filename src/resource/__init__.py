from flask import Blueprint

from .auth import auth_router
from .taxi import taxi_router
from . import chat

router = Blueprint("router", __name__, url_prefix="/api")

router.register_blueprint(auth_router, url_prefix="/taxi_auth")
router.register_blueprint(taxi_router, url_prefix="/taxi_info")
