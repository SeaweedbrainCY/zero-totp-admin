from flask_sqlalchemy import SQLAlchemy
from zero_totp_db_model.model import User
from main import db


def get_all_users():
    return db.session.query(User).all()