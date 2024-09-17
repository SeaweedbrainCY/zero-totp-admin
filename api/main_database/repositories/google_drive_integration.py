from zero_totp_db_model.model import GoogleDriveIntegration
from main import db


def is_google_drive_enabled_by_userid(user_id):
    integration = db.session.query(GoogleDriveIntegration).filter(GoogleDriveIntegration.user_id == user_id).first()
    return integration.isEnabled if integration else False