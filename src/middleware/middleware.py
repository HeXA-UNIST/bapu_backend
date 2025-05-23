from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from flask_admin import Admin

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
migrate = Migrate()
session = Session()
admin = Admin(name="BAPU_ADMIN", template_mode="bootstrap3")
