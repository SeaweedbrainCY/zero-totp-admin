import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import Notifications
from admin_database.models import Admin as AdminModel, Session as SessionModel
from environment.configuration import conf
from uuid import uuid4
import datetime as dt
import json

class TestGetNotification(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/notification/"
        self.notif = {
             "id": str(uuid4()),
                "message": "My notif",
                "timestamp": str(dt.datetime.now(dt.UTC).timestamp()),
                "expiration_timestamp": str(dt.datetime.now(dt.UTC).timestamp()),
                "enabled": True,
        }
        self.session_id = str(uuid4())
        self.admin_id = str(uuid4())

        
        with self.application.app_context():
            db.create_all()
            other_notif = Notifications(id=str(uuid4()), message="Hello, World!", timestamp=dt.datetime.now(dt.UTC), expiry=dt.datetime.now(dt.UTC), enabled=True, authenticated_user_only=False)

            notif = Notifications(id=self.notif["id"], message=self.notif["message"], timestamp=self.notif["timestamp"], expiry=self.notif["expiration_timestamp"], enabled=self.notif["enabled"], authenticated_user_only=False)
            
            another_notif = Notifications(id=str(uuid4()), message="Hello, World!", timestamp=dt.datetime.now(dt.UTC), expiry=dt.datetime.now(dt.UTC), enabled=True, authenticated_user_only=False)

            admin = AdminModel(id=self.admin_id, username="root", password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=self.admin_id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)

            db.session.add(other_notif)
            db.session.add(notif)
            db.session.add(another_notif)
            db.session.commit()
    
    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()
    
    def test_get_notification_by_id(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}{self.notif['id']}")
            self.assertEqual(response.status_code, 200)
            for key in self.notif.keys():
                self.assertEqual(response.json()[key], self.notif[key])