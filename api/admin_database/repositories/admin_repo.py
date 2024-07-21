from flask_sqlalchemy import SQLAlchemy
from ..models import Admin
from main import db


def get_user_by_username(username):
    return db.session.query(Admin).filter(Admin.username == username).first()

def get_user_by_id(id):
     return db.session.query(Admin).filter(Admin.id == id).first()
