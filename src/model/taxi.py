from uuid import uuid4
from datetime import datetime
from typing import Union

from src.middleware import db


class TaxiPool(db.Model):
    __tablename__ = "taxi_pool"  # 테이블 이름
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 기본 키
    start_position = db.Column(db.String(30), nullable=False)  # 출발 위치
    end_position = db.Column(db.String(30), nullable=False)  # 도착 위치
    total_people = db.Column(db.Integer, nullable=False)  # 모집 인원
    start_time = db.Column(db.DateTime, nullable=False)  # 출발 시간
    status = db.Column(db.Integer, nullable=False, default=0)  # 상태
    creator_id = db.Column(db.Integer, nullable=False)  # 생성자
    room_id = db.Column(db.String(30), nullable=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 생성시간

    def create(self, start_position: str, end_position: str, total_people: int, start_time: str, creator_id: str) -> "TaxiPool":
        self.start_position = start_position
        self.end_position = end_position
        self.total_people = total_people
        self.start_time = start_time
        self.creator_id = creator_id
        db.session.add(self)
        db.session.commit()
        return self

    
    @classmethod
    def select_taxi_pools_by_day(cls, start_date: datetime, end_date: datetime, order_by_start_time_asc: bool = True) -> list["TaxiPool"]:
        taxi_pools = cls.query.filter(start_date <= cls.start_time, cls.start_time <= end_date)
        if order_by_start_time_asc:
            taxi_pools = taxi_pools.order_by(cls.start_time.asc())
        taxi_pools = taxi_pools.all()
        return taxi_pools

    @classmethod
    def select_taxi_pool_by_id(cls, id: str) -> Union["TaxiPool", None]:
        taxi_pool = cls.query.filter(cls.id == id).first()
        return taxi_pool

    def as_dict(self) -> dict:
        return {
            # "id": self.id,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "total_people": self.total_people,
            "start_time": self.start_time,
            "status": self.status,
            # "creator_id": self.creator_id,
            # "room_id": self.room_id,
            # "creator_nickname": self.creator_nickname,
            "created_at": self.created_at,
        }


class PoolMember(db.Model):
    __tablename__ = "pool_member"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taxi_id = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)

    def create(self, taxi_id: int, user_id: int) -> "PoolMember":
        self.taxi_id = taxi_id
        self.user_id = user_id
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def count_pool_member(cls, taxi_id: int) -> int:
        pool_member = cls.query.filter(cls.taxi_id == taxi_id).count()
        return pool_member

    @classmethod
    def select_pool_member_by_taxi_user_id(cls, user_id: int, taxi_id: int) -> Union["PoolMember", None]:
        pool_member = cls.query.filter(cls.user_id == user_id, cls.taxi_id == taxi_id).first()
        return pool_member
