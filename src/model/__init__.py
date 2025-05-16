from .auth import Auth, User
from .taxi import PoolMember, TaxiPool
from .chat import Chat

# init admin
from flask_admin.contrib.sqla import ModelView
from src.middleware import admin
from src.middleware import db

admin.add_view(ModelView(Auth, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(PoolMember, db.session))
admin.add_view(ModelView(TaxiPool, db.session))
admin.add_view(ModelView(Chat, db.session))
