import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import Notifications
from admin_database.models import Admin as AdminModel, Session as SessionModel
from environment.configuration import conf
from uuid import uuid4
import datetime as dt
import json

class TestCreateNotification(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/notification"
        self.session_id = str(uuid4())
        self.admin_id = str(uuid4())

        
        with self.application.app_context():
            db.create_all()
            other_notif = Notifications(id=str(uuid4()), message="Hello, World!", timestamp=dt.datetime.now(dt.UTC), expiry=dt.datetime.now(dt.UTC), enabled=True, authenticated_user_only=False)
            
            another_notif = Notifications(id=str(uuid4()), message="Hello, World!", timestamp=dt.datetime.now(dt.UTC), expiry=dt.datetime.now(dt.UTC), enabled=True, authenticated_user_only=False)

            admin = AdminModel(id=self.admin_id, username="root", password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=self.admin_id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)

            db.session.add(other_notif)
            db.session.add(another_notif)
            db.session.commit()
    
    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()
    
    def test_create_notification(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.post(self.endpoint, json={"message": "Hello, World!"})
            self.assertEqual(response.status_code, 201)
            response_data = response.json()
            self.assertEqual(response_data["message"], "Hello, World!")
            self.assertEqual(response_data["enabled"], False)
            self.assertEqual(response_data["auth_user_only"], False)
            self.assertIsNotNone(response_data["id"], "Was expecting an id but got None")
            self.assertIsNotNone(response_data["timestamp"],  "Was expecting timestamp but got None")
            self.assertIsNone(response_data["expiration_timestamp"],  f"Was expecting expiration_timestamp at None but got {response_data['expiration_timestamp']}")
    
    def test_create_notification_with_expiry(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            expiry = dt.datetime.now(dt.UTC).timestamp()
            response = self.client.post(self.endpoint, json={"message": "Hello, World!", "expiration_timestamp_utc": expiry})
            self.assertEqual(response.status_code, 201)
            response_data = response.json()
            self.assertEqual(response_data["message"], "Hello, World!")
            self.assertEqual(response_data["enabled"], False)
            self.assertEqual(response_data["auth_user_only"], False)
            self.assertEqual(response_data["expiration_timestamp"][:10],  str(expiry)[:10]) # We are comparing the timestamp without the milliseconds
            self.assertIsNotNone(response_data["id"], "Was expecting an id but got None")
            self.assertIsNotNone(response_data["timestamp"],  "Was expecting timestamp but got None")
    
    def test_create_notification_with_enabled(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.post(self.endpoint, json={"message": "Hello, World!", "enabled": True})
            self.assertEqual(response.status_code, 201)
            response_data = response.json()
            self.assertEqual(response_data["message"], "Hello, World!")
            self.assertEqual(response_data["enabled"], True)
            self.assertEqual(response_data["auth_user_only"], False)
            self.assertIsNotNone(response_data["id"], "Was expecting an id but got None")
            self.assertIsNotNone(response_data["timestamp"],  "Was expecting timestamp but got None")
            self.assertIsNone(response_data["expiration_timestamp"],  f"Was expecting expiration_timestamp at None but got {response_data['expiration_timestamp']}")
    
    def test_create_notification_with_auth_user_only(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.post(self.endpoint, json={"message": "Hello, World!", "auth_user_only": True})
            self.assertEqual(response.status_code, 201)
            response_data = response.json()
            self.assertEqual(response_data["message"], "Hello, World!")
            self.assertEqual(response_data["enabled"], False)
            self.assertEqual(response_data["auth_user_only"], True)
            self.assertIsNotNone(response_data["id"], "Was expecting an id but got None")
            self.assertIsNotNone(response_data["timestamp"],  "Was expecting timestamp but got None")
            self.assertIsNone(response_data["expiration_timestamp"],  f"Was expecting expiration_timestamp at None but got {response_data['expiration_timestamp']}")
    
    def test_create_notification_with_all_fields(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            expiry = dt.datetime.now(dt.UTC).timestamp()
            response = self.client.post(self.endpoint, json={"message": "Hello, World!", "expiration_timestamp_utc": expiry, "enabled": True, "auth_user_only": True})
            self.assertEqual(response.status_code, 201)
            response_data = response.json()
            self.assertEqual(response_data["message"], "Hello, World!")
            self.assertEqual(response_data["enabled"], True)
            self.assertEqual(response_data["auth_user_only"], True)
            self.assertEqual(response_data["expiration_timestamp"][:10],  str(expiry)[:10])
            self.assertIsNotNone(response_data["id"], "Was expecting an id but got None")
            self.assertIsNotNone(response_data["timestamp"],  "Was expecting timestamp but got None")
