from flask import Blueprint, request
from datetime import datetime
from src.model import Rest
from src.middleware import db

rest_api = Blueprint("rest_api", __name__, url_prefix="/rest")


# 식당 정보 불러오는 api 작성

@rest_api.route("/get", methods=["GET"])
def get_rest_info():
    # get query string
    #start_date = request.args.get("start_date", "1999-01-01")
    #end_date = request.args.get("end_date", "2100-01-01")

    # convert to date
    #start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    #end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # get menu
    rests = Rest.query.all()

    # convert to dict
    rests = [
        {
            "restaurant_name": rest.rest_name,
            "meal_type": rest.meal_type,
            "price": rest.price,
            "open_time": rest.open_time,
            "close_time": rest.close_time,
        }
        for rest in rests
    ]

    return rests


@rest_api.route("/set", methods=["POST"])
def set_rest_info():
    # get json data
    data = request.get_json()

    rests = [Rest(**rest) for rest in data]
    db.session.add(rests)
    db.session.commit()

    return {"message": "success"}
