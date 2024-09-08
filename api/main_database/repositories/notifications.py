from zero_totp_db_model.model import Notifications
from main import db

def get_notification_by_id(notif_id):
    return db.session.query(Notifications).filter_by(id=notif_id).first()