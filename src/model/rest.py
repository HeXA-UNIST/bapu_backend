from src.middleware import db

from datetime import datetime


class TimeMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 생성 시간
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)  # 수정 시간

class Rest(db.Model, TimeMixin):
    __tablename__ = "REST"
    rest_id = db.Column(db.Integer, primary_key=True, index=True)
    rest_name = db.Column(db.String(100), nullable=False)
    meal_type = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)