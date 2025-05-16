from datetime import datetime, timedelta
from flask import Blueprint, session, request
from src.utils import AuthManager, auth_required
from src.error import handle_exceptions
from src.schema import CreateTaxiInfoSchema, GetTaxiInfoSchema, TaxiParticipateTaxiSchema
from src.model import TaxiPool, PoolMember, User

taxi_router = Blueprint("taxi", __name__)
auth_manager = AuthManager(session)
create_taxi_info_schema = CreateTaxiInfoSchema()
get_taxi_info_schema = GetTaxiInfoSchema()
taxi_participate_taxi_schema = TaxiParticipateTaxiSchema()


@taxi_router.route("/create", methods=["POST"])
@handle_exceptions
@auth_required(auth_manager)
def create_taxi_info():
    data = request.get_json()
    create_taxi_info_schema.validate(data)
    data = create_taxi_info_schema.load(data)
    
    # TODO : nickname 제거하기 완
    creator_id = auth_manager.user_id
    new_pool = TaxiPool().create(**data, creator_id=creator_id)
    return {"taxi_id": new_pool.id, "room_id": new_pool.room_id}, 200


@taxi_router.route("/taxi_info", methods=["GET"])
@handle_exceptions
@auth_required(auth_manager)
def get_taxi_info():
    data = request.args
    get_taxi_info_schema.validate(data)
    data = get_taxi_info_schema.load(data)
    # TODO : 이거 고치기 완
    start_datetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=data.get("day"))
    end_datetime = start_datetime + timedelta(days=1)
    # start_datetime = data.get("start_datetime")
    # end_datetime = data.get("end_datetime")
    print(start_datetime, end_datetime)

    taxi_pools = TaxiPool.select_taxi_pools_by_day(start_datetime, end_datetime) # List[TaxiPool]
    
    # TODO : nickname 가져오는 로직 추가해야함. 완
    if len(taxi_pools) == 0:
        return {"msg": "팟이 없어요"}, 404
    

    result = {
        "taxi_list": [
            {
                **taxi_pool.as_dict(),
                "num_participation": PoolMember.count_pool_member(taxi_pool.id),
                "creator_nickname": User.select_by_id(taxi_pool.creator_id).nickname,
            }
            for taxi_pool in taxi_pools
        ]
    }
    return result, 200

# TODO : 개별 택시팟 아이디로 검색 완 -> test 해봐야 함
@taxi_router.route("/taxi_info/<int:taxi_id>", methods=["GET"])
@handle_exceptions
@auth_required(auth_manager)
def get_taxi_info_by_id(taxi_id):
    # taxi_id로 택시 정보를 DB에서 조회
    taxi_pool = TaxiPool.select_taxi_pool_by_id(taxi_id)
    if not taxi_pool:
        return {"msg": "존재하지 않는 택시팟입니다."}, 404

    # creator_id로 유저 정보 조회
    user = User.select_by_id(taxi_pool.creator_id)
    if not user:
        return {"msg": "유효하지 않은 택시팟 생성자입니다."}, 404

    # 참여 인원 수를 구함
    participation_num = PoolMember.count_pool_member(taxi_pool.id)

    # API 스펙에 맞게 결과를 구성
    result = {
        "start_position": taxi_pool.start_position,
        "end_position": taxi_pool.end_position,
        "total_people": taxi_pool.total_people,
        "participation_num": participation_num,
        "start_time": taxi_pool.start_time,  # 모델 필드명에 맞게 수정
        "creator_nickname": user.nickname,
    }

    return result, 200


@taxi_router.route("/participate", methods=["POST"])
@handle_exceptions
@auth_required(auth_manager)
def taxi_paticipate():
    data = request.get_json()
    taxi_participate_taxi_schema.validate(data)
    data = taxi_participate_taxi_schema.load(data)
    user_id = auth_manager.user_id
    taxi_id = data.get("taxi_id")
    PoolMember().create(taxi_id=taxi_id, user_id=user_id)
    taxi_pool = TaxiPool.select_taxi_pools_by_id(taxi_id)
    return {"taxi_id": taxi_id, "room_id": taxi_pool.room_id}, 200


@taxi_router.route("/participate", methods=["GET"])
@handle_exceptions
@auth_required(auth_manager)
def is_taxi_paticipate():
    data = request.args
    taxi_participate_taxi_schema.validate(data)
    data = taxi_participate_taxi_schema.load(data)
    user_id = auth_manager.user_id
    pool = PoolMember.select_pool_member_by_taxi_user_id(taxi_id=data.get("taxi_id"), user_id=user_id)
    return {"is_participated": True if pool else False}, 200
