import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import User, TOTP_secret, GoogleDriveIntegration
from environment.configuration import conf
from admin_database.models import Admin as AdminModel, Session as SessionModel
from uuid import uuid4
import datetime as dt
import json

class TestGetUserById(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/users/"
        self.session_id = str(uuid4())


        self.user_info = {
             "id":2,
             "username":"user2",
             "email":"users2@mail.com",
             "signup_date":"2021-10-10",
            "isVerified":True,
            "isBlocked":False, 
            "total_of_2fa":3,
            "is_google_drive_enabled":False,
            "last_login_date": dt.datetime.now(dt.UTC).timestamp()
        }
        with self.application.app_context():
            db.create_all()
            random_user = User(id=1, username=f"user1", mail=f"user1@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=False)
            db.session.add(random_user)

            interesting_user = User(id=self.user_info["id"], username=self.user_info["username"], mail=self.user_info["email"], password="random", passphraseSalt="doesn't matter", isVerified=self.user_info["isVerified"], derivedKeySalt="random", createdAt=self.user_info["signup_date"], isBlocked=self.user_info["isBlocked"], last_login_date= self.user_info["last_login_date"])
            db.session.add(interesting_user)
            for _ in range(self.user_info["total_of_2fa"]):
                db.session.add(TOTP_secret(uuid=str(uuid4()), user_id=self.user_info["id"], secret_enc="test_test"))
            db.session.add(GoogleDriveIntegration( user_id=self.user_info["id"], isEnabled=self.user_info["is_google_drive_enabled"]))
            

            admin = AdminModel(id=str(uuid4()), username="root", password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=admin.id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)
            db.session.commit()
    
    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()

    

    def test_get_user_by_id(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}{self.user_info['id']}")
            self.assertEqual(response.status_code, 200)
            for key in self.user_info.keys():
                if "last_login_date" == key:
                    self.assertEqual(response.json()[key], int(float(self.user_info[key])) if self.user_info[key]else 0)
                else:
                    self.assertEqual(response.json()[key], self.user_info[key])
    
    def test_get_user_by_id_not_found(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}3")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(), {"error": "User not found"})
    
    def test_get_user_by_id_no_totp_codes(self):
        with self.application.app_context():
            db.session.query(TOTP_secret).filter(TOTP_secret.user_id == self.user_info["id"]).delete()
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}{self.user_info['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["total_of_2fa"], 0)
    
    def test_get_user_by_id_no_integration(self):
        with self.application.app_context():
            db.session.query(GoogleDriveIntegration).filter(GoogleDriveIntegration.user_id == self.user_info["id"]).delete()
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}{self.user_info['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["is_google_drive_enabled"], False)
    
    def test_get_user_by_id_with_google_drive_enabled(self):
        with self.application.app_context():
            db.session.query(GoogleDriveIntegration).filter(GoogleDriveIntegration.user_id == self.user_info["id"]).delete()
            db.session.add(GoogleDriveIntegration( user_id=self.user_info["id"], isEnabled=True))
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}{self.user_info['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["is_google_drive_enabled"], True)
    
    def test_get_user_by_id_no_login_date(self):
        with self.application.app_context():
            db.session.query(User).filter(User.id == self.user_info["id"]).update({"last_login_date": None})
            db.session.commit()
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(f"{self.endpoint}{self.user_info['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["last_login_date"], 0)


