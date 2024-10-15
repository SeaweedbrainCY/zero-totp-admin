import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import User,  TOTP_secret, GoogleDriveIntegration
from environment.configuration import conf
from admin_database.models import Admin as AdminModel, Session as SessionModel
from uuid import uuid4
import datetime as dt
import json

class TestGetAllUsers(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/users/all"
        self.session_id = str(uuid4())

        self.users_info = [
            {
             "id":2,
             "username":"user2",
             "email":"users2@mail.com",
             "signup_date":"2021-10-10",
            "isVerified":True,
            "isBlocked":False, 
            "total_of_2fa":3,
            "is_google_drive_enabled":False,
            "last_login_date": dt.datetime.now(dt.UTC).timestamp()
            },
            {
             "id":1,
             "username":"user1",
             "email":"users1@mail.com",
             "signup_date":"2022-10-10",
            "isVerified":True,
            "isBlocked":True,
            "total_of_2fa":0,
            "is_google_drive_enabled":False,
            "last_login_date": None
            },
            {
             "id":22,
             "username":"user22",
             "email":"users22@mail.com",
             "signup_date":"2021-12-10",
            "isVerified":True,
            "isBlocked":False,
            "total_of_2fa":20,
            "is_google_drive_enabled":False,
            "last_login_date": dt.datetime.now(dt.UTC).timestamp()
            },
            {
             "id":90,
             "username":"user90",
             "email":"users90@mail.com",
             "signup_date":"2021-10-31",
            "isVerified":False,
            "isBlocked":False,
            "total_of_2fa":10,
            "is_google_drive_enabled":False,
            "last_login_date": dt.datetime.now(dt.UTC).timestamp()
            },
            {
             "id":62,
             "username":"user62",
             "email":"users62@mail.com",
             "signup_date":"2024-10-10",
            "isVerified":False,
            "isBlocked":True,
            "total_of_2fa":0,
            "is_google_drive_enabled":True,
            "last_login_date": None
            },
            {
             "id":20,
             "username":"user20",
             "email":"users20@mail.com",
             "signup_date":"2021-20-10",
            "isVerified":True,
            "isBlocked":False,
            "total_of_2fa":1,
            "is_google_drive_enabled":False,
            "last_login_date": dt.datetime.now(dt.UTC).timestamp()
            },

        ]
        with self.application.app_context():
            db.create_all()
            for user in self.users_info:
                user_obj = User(id=user["id"], username=user["username"], mail=user["email"], password="random", passphraseSalt="doesn't matter", isVerified=user["isVerified"], derivedKeySalt="doesn't matter", createdAt=user["signup_date"], isBlocked=user["isBlocked"], last_login_date=user["last_login_date"])
                for _ in range(user["total_of_2fa"]):
                    db.session.add(TOTP_secret(uuid=str(uuid4()), user_id=user["id"], secret_enc="test_test"))
                db.session.add(GoogleDriveIntegration( user_id=user["id"], isEnabled=user["is_google_drive_enabled"]))
                db.session.add(user_obj)


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
            response = self.client.get(self.endpoint)
            self.assertEqual(response.status_code, 200)
            returned_users = response.json()["users"]
            for user in self.users_info:
                infos = {}
                for returned_user in returned_users:
                    if returned_user["id"] == user["id"]:
                        infos = returned_user
                        break
                self.assertNotEqual(infos, {}, f"User not found. Was looking for user with id {user['id']} in {returned_users}")
                for key in user.keys():
                    self.assertEqual(infos[key], user[key])
    


