import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import Notifications
from admin_database.models import Admin as AdminModel, Session as SessionModel
from environment.configuration import conf
from uuid import uuid4
import datetime as dt
import json

class TestUpdateNotification(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/notification"
        self.session_id = str(uuid4())
        self.admin_id = str(uuid4())
        self.notif = {
             "id": str(uuid4()),
                "message": "My notif",
                "timestamp": str(dt.datetime.now(dt.UTC).timestamp()),
                "expiration_timestamp": str(dt.datetime.now(dt.UTC).timestamp() + 3600),
                "enabled": True,
                "auth_user_only": False
        }

        
        with self.application.app_context():
            db.create_all()
            other_notif = Notifications(id=str(uuid4()), message="Hello, World!", timestamp=dt.datetime.now(dt.UTC), expiry=dt.datetime.now(dt.UTC), enabled=True, authenticated_user_only=False)
            another_notif = Notifications(id=str(uuid4()), message="Hello, World!", timestamp=dt.datetime.now(dt.UTC), expiry=dt.datetime.now(dt.UTC), enabled=True, authenticated_user_only=False)
            notif = Notifications(id=self.notif["id"], message=self.notif["message"], timestamp=self.notif["timestamp"], expiry=self.notif["expiration_timestamp"], enabled=self.notif["enabled"], authenticated_user_only=False)


            admin = AdminModel(id=self.admin_id, username="root", password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=self.admin_id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)
            db.session.add(notif)
            db.session.add(other_notif)
            db.session.add(another_notif)
            db.session.commit()
    
    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()
    
    def test_update_notification(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"message": "Hello, World!2"})
            print("response_data", response.json())
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertEqual(response_data["message"], "Hello, World!2")
            self.assertEqual(response_data["enabled"], self.notif["enabled"])
            self.assertEqual(response_data["auth_user_only"], self.notif["auth_user_only"])
            self.assertEqual(response_data["expiration_timestamp"][:10],  str(self.notif["expiration_timestamp"])[:10]) 
            self.assertEqual(response_data["id"], self.notif["id"])
            self.assertEqual(response_data["timestamp"], self.notif["timestamp"])


    def test_update_notification_with_expiry(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            expiry = dt.datetime.now(dt.UTC).timestamp()  + 3600
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"expiration_timestamp_utc": expiry})
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertEqual(response_data["message"], self.notif["message"])
            self.assertEqual(response_data["enabled"], self.notif["enabled"])
            self.assertEqual(response_data["auth_user_only"], self.notif["auth_user_only"])
            self.assertEqual(response_data["expiration_timestamp"][:10],  str(expiry)[:10]) 
            self.assertEqual(response_data["id"], self.notif["id"])
            self.assertEqual(response_data["timestamp"], self.notif["timestamp"])
    
    def test_update_notification_with_enabled(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"enabled": False})
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertEqual(response_data["message"], self.notif["message"])
            self.assertEqual(response_data["enabled"], False)
            self.assertEqual(response_data["auth_user_only"], self.notif["auth_user_only"])
            self.assertEqual(response_data["expiration_timestamp"][:10],  str(self.notif["expiration_timestamp"])[:10]) 
            self.assertEqual(response_data["id"], self.notif["id"])
            self.assertEqual(response_data["timestamp"], self.notif["timestamp"])
    
    def test_update_notification_with_auth_user_only(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"auth_user_only": True})
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertEqual(response_data["message"], self.notif["message"])
            self.assertEqual(response_data["enabled"], self.notif["enabled"])
            self.assertEqual(response_data["auth_user_only"], True)
            self.assertEqual(response_data["expiration_timestamp"][:10],  str(self.notif["expiration_timestamp"])[:10]) 
            self.assertEqual(response_data["id"], self.notif["id"])
            self.assertEqual(response_data["timestamp"], self.notif["timestamp"])
    
    def test_update_notification_with_empty_message(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"message": ""})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["error"], "Message cannot be empty")
    
    def test_update_notification_with_long_message(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"message": "a"*766})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["error"], "Message cannot be longer than 765 characters")
    
    def test_update_notification_with_past_expiration(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            expiry = dt.datetime.now(dt.UTC).timestamp() - 1
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"expiration_timestamp_utc": expiry})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["error"], "Expiration date must be in the future")
    
    def test_update_notification_with_future_expiration_too_long(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            expiry = dt.datetime.now(dt.UTC).timestamp() + 365*6*24*60*60 + 1
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"expiration_timestamp_utc": expiry})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["error"], "Expiration date cannot be more than 5 years in the future. Set expiration to None to keep a notification indefinitely.")
    
    def test_update_notification_not_found(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{str(uuid4())}", json={"message": "Hello, World!"})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["error"], "Notification not found")

    
    def test_update_notification_with_invalid_expiry(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"expiration_timestamp_utc": "invalid"})
            self.assertEqual(response.status_code, 400)
    
    def test_update_notification_with_invalid_expiry_type(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"expiration_timestamp_utc": "100000000000"})
            self.assertEqual(response.status_code, 400)
    
    def test_update_notification_with_invalid_enabled_type(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"enabled": "True"})
            self.assertEqual(response.status_code, 400)
    
    def test_update_notification_with_invalid_auth_user_only_type(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"auth_user_only": "True"})
            self.assertEqual(response.status_code, 400)
    
    def test_update_notification_with_invalid_message_type(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}/{self.notif['id']}", json={"message": True})
            self.assertEqual(response.status_code, 400)
    

    
