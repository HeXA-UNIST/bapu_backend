from flask import Blueprint
from .menu import menu_api
from .rest import rest_api
from .notification import noti_api

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(menu_api)
api.register_blueprint(rest_api)
api.register_blueprint(noti_api)
