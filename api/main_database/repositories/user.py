from flask_sqlalchemy import SQLAlchemy
from zero_totp_db_model.model import User, ZKE_encryption_key,TOTP_secret,GoogleDriveIntegration,Preferences,EmailVerificationToken,RateLimiting
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
    db.session.query(ZKE_encryption_key).filter(ZKE_encryption_key.user_id == user_id).delete()
    db.session.query(TOTP_secret).filter(TOTP_secret.user_id == user_id).delete()
    db.session.query(GoogleDriveIntegration).filter(GoogleDriveIntegration.user_id == user_id).delete()
    db.session.query(Preferences).filter(Preferences.user_id == user_id).delete()
    db.session.query(EmailVerificationToken).filter(EmailVerificationToken.user_id == user_id).delete()
    db.session.query(RateLimiting).filter(RateLimiting.user_id == user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return True