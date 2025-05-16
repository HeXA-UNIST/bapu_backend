from typing import Union
from datetime import datetime

from src.middleware import db


class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String, nullable=False, index=True)  # 이메일 주소
    otp = db.Column(db.String, nullable=False)  # 인증 번호
    is_verified = db.Column(db.Boolean, nullable=False, default=False)  # 인증 성공 여부
    num_tries = db.Column(db.Integer, nullable=False, default=0)  # 인증 시도 횟수
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 인증 생성 시간

    def create(self, email: str, otp: str, is_verified: bool = False) -> "Auth":
        self.email = email
        self.otp = otp
        self.is_verified = is_verified
        db.session.add(self)
        db.session.commit()
        return self

    def update_is_verified(self, is_verified: bool) -> None:
        self.is_verified = is_verified
        db.session.commit()

    @classmethod
    def select_by_email(cls, email: str) -> Union["Auth", None]:
        return cls.query.filter(cls.email == email).order_by(cls.created_at.desc()).first()

    @classmethod
    def select_by_nickname(cls, nickname: int) -> Union["User", None]:
        return cls.query.filter(cls.nickname == nickname).first()

    def update_num_tries(self) -> None:
        self.num_tries += 1
        db.session.commit()


class User(db.Model):
    __tablename__ = "user"  # 테이블 이름
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String, nullable=False, unique=True, index=True)  # 이메일 주소
    nickname = db.Column(db.String, nullable=False, unique=True, index=True)  # 닉네임
    is_banned = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 계정 생성 시간

    def create(self, email: str, nickname: str) -> None:
        self.email = email
        self.nickname = nickname
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def select_by_email(cls, email: str) -> Union["User", None]:
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def select_by_nickname(cls, nickname: str) -> Union["User", None]:
        return cls.query.filter(cls.nickname == nickname).first()

    @classmethod
    def select_by_id(cls, id: int) -> Union["User", None]:
        return cls.query.filter(cls.id == id).first()


    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname,
            "is_banned": self.is_banned,
            # "created_at": self.created_at,
        }
