from flask import Blueprint
from .menu import menu_api

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(menu_api)
