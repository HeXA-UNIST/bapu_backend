from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_admin import Admin

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
migrate = Migrate()
socketio = SocketIO(manage_session=False, cors_allowed_origins="*")
session = Session()
admin = Admin(name="TaxiHeXA", template_mode="bootstrap3")
mail = Mail()
