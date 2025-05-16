from flask_socketio import join_room, leave_room, rooms, emit
from flask import session, request

from src.middleware import socketio
from src.schema import EnterRoomSchema, SendMessageSchema
from src.error import handle_exceptions_on_socketio
from src.model import Chat
from src.utils import AuthManager, auth_required_on_socketio

from src.model import User

enter_room_schema = EnterRoomSchema()
send_message_schema = SendMessageSchema()
auth_manager = AuthManager(session)


@socketio.on("connect")
def connect(data):
    return


@socketio.on("status")
def server_status(data):
    emit("status", {"status": "ok"})


@socketio.on("auth_info")
@auth_required_on_socketio(auth_manager)
def auth_info(data):
    emit("info", auth_manager.get_user_info().as_dict())


@socketio.on("join_room")
@handle_exceptions_on_socketio
@auth_required_on_socketio(auth_manager)
def enter_room(data):
    user_rooms = rooms(request.sid)
    if len(user_rooms) >= 1:
        socketio.emit("info", {"msg": "방을 목록을 초기화합니다."})
        for room in user_rooms:
            leave_room(room)

    data = enter_room_schema.load(data)
    user_id = auth_manager.user_id
    room_id = data.get("room_id")
    join_room(room_id)

    prev_chats = Chat.select_by_room_id(room_id=room_id)

    res = []
    for chat in prev_chats:
        c = {
            "nickname": chat.nickname,
            "is_me": user_id == chat.user_id,
            "content": chat.content,
            "created_at": chat.created_at,
        }
        res.append(c)
    socketio.emit("prev_chats", res)


@socketio.on("send_message")
@handle_exceptions_on_socketio
@auth_required_on_socketio(auth_manager)
def chat_message(data):
    user_rooms = rooms(request.sid)
    # TODO : user_rooms의 길이가 0인경우를 고려해야함. 대충 완
    if len(user_rooms) == 0:
        socketio.emit(
            "error",
            {"msg": "참여 중인 방이 없습니다. 메시지를 전송할 수 없습니다."},
            to=request.sid
        )
        return
    if len(user_rooms) > 1:
        socketio.emit("error", {"msg": "비정상적인 접근입니다. 방을 목록을 초기화합니다."})
        for room in user_rooms:
            leave_room(room)
        return

    room_id = user_rooms[0]
    data = send_message_schema.load(data)
    content = data.get("content")

    chat = Chat().create(
        user_id=auth_manager.user_id,
        nickname=auth_manager.nickname,
        room_id=room_id,
        content=content,
    )

    socketio.emit(
        "new_message",
        {
            "is_me": True,
            "nickname": chat.nickname,
            "content": chat.content,
            "created_at": str(chat.created_at),
        },
        to=request.sid,
    )

    socketio.emit(
        "new_message",
        {
            "is_me": False,
            "nickname": chat.nickname,
            "content": chat.content,
            "created_at": str(chat.created_at),
        },
        room=room_id,
        skip_sid=request.sid,
    )


@socketio.on("leave_room")
@handle_exceptions_on_socketio
@auth_required_on_socketio(auth_manager)
def exit_room(data):
    user_rooms = rooms(request.sid)
    for room in user_rooms:
        leave_room(room)
