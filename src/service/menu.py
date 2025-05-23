from flask import Blueprint, request
from datetime import datetime
from src.model import Menu
from src.middleware import db

menu_api = Blueprint("menu_api", __name__, url_prefix="/menu")


@menu_api.route("/get", methods=["GET"])
def get_menu():
    # get query string
    start_date = request.args.get("start_date", "1999-01-01")
    end_date = request.args.get("end_date", "2100-01-01")

    # convert to date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # get menu
    menus = Menu.query.filter(Menu.date >= start_date, Menu.date <= end_date).all()

    # convert to dict
    menus = [
        {
            "display_restaurant": menu.display_restaurant,
            "display_menu": menu.display_menu,
            "kcal": menu.kcal,
            "date": menu.date.strftime("%Y-%m-%d"),
            "meal_type": menu.meal_type,
        }
        for menu in menus
    ]

    return menus


@menu_api.route("/set", methods=["POST"])
def set_menu():
    # get json data
    data = request.get_json()

    menus = [Menu(**menu) for menu in data]
    db.session.add(menus)
    db.session.commit()

    return {"message": "success"}
