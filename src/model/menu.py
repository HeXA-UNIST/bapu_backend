from src.middleware import db

from datetime import datetime


class TimeMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 생성 시간
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)  # 수정 시간


class Menu(db.Model, TimeMixin):
    __tablename__ = "menu"
    menu_id = db.Column(db.Integer, primary_key=True, index=True)
    display_restaurant = db.Column(db.String(100), nullable=False)
    display_menu = db.Column(db.String(500), nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.Integer, nullable=False)
