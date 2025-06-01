from flask import Blueprint, request
from datetime import datetime
from src.model import Noti
from src.middleware import db
from sqlalchemy import or_

noti_api = Blueprint("noti_api", __name__, url_prefix="/noti")


@noti_api.route("/get", methods=["GET"])
def get_noti():

    today= datetime.today().date()

    # get menu
    notis = Noti.query.filter(or_(
        Noti.noti_due == None,
        Noti.noti_due >= today,
    )).all()

    # convert to dict
    notis = [
        {
            "noti_title": noti.noti_title,
            "noti_text": noti.noti_text,
        }
        for noti in notis
    ]

    return notis


@noti_api.route("/set", methods=["POST"])
def set_noti():
    # get json data
    data = request.get_json()

    notis = [Noti(**noti) for noti in data]
    db.session.add(notis)
    db.session.commit()

    return {"message": "success"}
