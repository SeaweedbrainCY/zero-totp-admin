from flask_sqlalchemy import SQLAlchemy
from zero_totp_db_model.model import User
from main import db


def get_all_users():
    return db.session.query(User).all()

def get_user_by_id(user_id):
    return db.session.query(User).filter(User.id == user_id).first()

def block_user_by_id(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.isBlocked = True
    db.session.commit()
    return user