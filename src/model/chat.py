from datetime import datetime
from typing import List

from src.middleware import db


class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True, index=True)
    room_id = db.Column(db.String)
    user_id = db.Column(db.Integer)
    nickname = db.Column(db.String)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)

    def create(self, user_id: int, nickname: str, room_id: str, content: str) -> "Chat":
        self.user_id = user_id
        self.nickname = nickname
        self.room_id = room_id
        self.content = content
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def select_by_room_id(cls, room_id: str, limit: int = 1000) -> List["Chat"]:
        return cls.query.filter(cls.room_id == room_id).order_by(cls.created_at.desc()).limit(limit).all()

    def as_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "user_id": self.user_id,
            "nickname": self.nickname,
            "content": self.content,
            "created_at": self.created_at,
        }
