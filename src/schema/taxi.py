from src.middleware import ma
from datetime import datetime

from src.error import InvalidTimeError


def validate_day_form(day: str):
    try:
        day_obj = datetime.strptime(day, "%Y-%m-%d-%H-%M")
        return day_obj
    except:
        raise InvalidTimeError


class CreateTaxiInfoSchema(ma.Schema):
    start_position = ma.Str(required=True)
    end_position = ma.Str(required=True)
    total_people = ma.Int(required=True)
    start_time = ma.DateTime(required=True)


class GetTaxiInfoSchema(ma.Schema):
    day = ma.Int(required=True)
    # start_datetime = ma.DateTime(required=True, validate=[validate_day_form])
    # end_datetime = ma.DateTime(required=True, validate=[validate_day_form])


class TaxiParticipateTaxiSchema(ma.Schema):
    taxi_id = ma.Str(required=True)
