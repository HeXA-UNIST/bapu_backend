from flask_admin.contrib.sqla import ModelView
from src.middleware import admin, db
from .menu import Menu
from .rest import Rest

admin.add_view(ModelView(Menu, db.session))
admin.add_view(ModelView(Rest, db.session))
