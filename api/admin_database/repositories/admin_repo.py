from flask_sqlalchemy import SQLAlchemy
from ..models import Admin
from main import db


def get_user_by_username(id):
    return db.session.query(Admin).filter(Admin.username == id).first()