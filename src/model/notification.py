from time import timezone

from src.middleware import db

from datetime import datetime


class TimeMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 생성 시간
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)  # 수정 시간


class Noti(db.Model, TimeMixin):
    __tablename__ = "Notification"
    noti_id = db.Column(db.Integer, primary_key=True, index=True)
    noti_title = db.Column(db.String(500), nullable=False)
    noti_text = db.Column(db.String(500), nullable=False)
    noti_due = db.Column(db.DateTime(timezone=True))
