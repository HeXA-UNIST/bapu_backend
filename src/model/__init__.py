from flask_admin.contrib.sqla import ModelView
from src.middleware import admin, db
from .menu import Menu

admin.add_view(ModelView(Menu, db.session))
