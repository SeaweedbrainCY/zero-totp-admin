from zero_totp_db_model.model import Notifications
from main import db
import datetime as dt
from uuid import uuid4

def get_notification_by_id(notif_id):
    return db.session.query(Notifications).filter_by(id=notif_id).first()

def create_notification(message, expiry=None, enabled=False, authenticated_user_only=False):
    timestamp = str(dt.datetime.now(dt.UTC).timestamp())
    id = str(uuid4())
    notif = Notifications(id=id, timestamp=timestamp, message=message, expiry=expiry, enabled=enabled, authenticated_user_only=authenticated_user_only)
    db.session.add(notif)
    db.session.commit()
    return notif

def get_all_notifications():
    return db.session.query(Notifications).all()