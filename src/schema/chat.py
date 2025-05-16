from src.middleware import ma


class EnterRoomSchema(ma.Schema):
    room_id = ma.Str(required=True)


class SendMessageSchema(ma.Schema):
    content = ma.Str(required=True)
