from zero_totp_db_model.model import RateLimiting
from main import db


def get_rate_limited_ip():
    return db.session.query(RateLimiting).filter_by(action_type="failed_login").all()

def get_rate_limited_emails():
    return db.session.query(RateLimiting).filter_by(action_type="send_verification_email").all()