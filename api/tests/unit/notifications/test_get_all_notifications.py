import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import Notifications
from admin_database.models import Admin as AdminModel, Session as SessionModel
from environment.configuration import conf
from uuid import uuid4
import datetime as dt
import json

class TestGetAllNotifications(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/notifications/all"
        self.notifs = {}
        for i in range(10):
            notif = {
                "id": str(uuid4()),
                "message": f"My notif {i}",
                "timestamp": str(dt.datetime.now(dt.UTC).timestamp()),
                "expiration_timestamp": str(dt.datetime.now(dt.UTC).timestamp()) if i % 2 == 1 else None,
                "enabled": True if i % 2 == 0 else False,
                "authenticated_user_only": False if i % 2 == 0 else True
            }
            self.notifs[notif["id"]] = notif
        self.session_id = str(uuid4())
        self.admin_id = str(uuid4())

        
        with self.application.app_context():
            db.create_all()
            for notif in self.notifs.values():
                db.session.add(Notifications(id=notif["id"], message=notif["message"], timestamp=notif["timestamp"], expiry=notif["expiration_timestamp"], enabled=notif["enabled"], authenticated_user_only=notif["authenticated_user_only"]))

            admin = AdminModel(id=self.admin_id, username="root", password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=self.admin_id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)

            db.session.commit()
    
    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()
    
    def test_get_all_notifs(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(self.endpoint)
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertEqual(len(response_data["notifications"]), 10)
            for notif in response_data["notifications"]:
                self.assertEqual(notif["message"], self.notifs[notif["id"]]["message"])
                self.assertEqual(notif["timestamp"], self.notifs[notif["id"]]["timestamp"])
                self.assertEqual(notif["expiration_timestamp"], self.notifs[notif["id"]]["expiration_timestamp"])
                self.assertEqual(notif["enabled"], self.notifs[notif["id"]]["enabled"])
                self.assertEqual(notif["auth_user_only"], self.notifs[notif["id"]]["authenticated_user_only"])
    
    def test_get_all_notifs_not_found(self):
        with self.application.app_context():
            db.session.query(Notifications).delete()
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}")
            self.assertEqual(response.status_code, 404)
            response_data = response.json()
            self.assertEqual(response_data["error"], "Notifications not found")