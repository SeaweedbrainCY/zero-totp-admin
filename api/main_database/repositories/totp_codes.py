from zero_totp_db_model.model import TOTP_secret
from main import db


def count_totp_secrets_by_user_id(user_id):
    return db.session.query(TOTP_secret).filter(TOTP_secret.user_id == user_id).count()