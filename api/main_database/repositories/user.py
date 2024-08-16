from flask_sqlalchemy import SQLAlchemy
from zero_totp_db_model.model import User
from main import db


def get_all_users():
    return db.session.query(User).all()

def get_user_by_id(user_id):
    return db.session.query(User).filter(User.id == user_id).first()

def update_blocked_status_by_userid(user_id, is_blocked):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.isBlocked = is_blocked
    db.session.commit()
    return user

def delete_user_by_id(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.session.delete(user)
    db.session.commit()
    return True