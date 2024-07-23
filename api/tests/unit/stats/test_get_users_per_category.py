import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import User
from environment.configuration import conf
from admin_database.models import Admin as AdminModel, Session as SessionModel
from admin_database.repositories import session as session_repo
from uuid import uuid4
import datetime as dt
import json


class TestGetUserPerCategory(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception("Test must be run with in memory database")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/stats/users/category"

        self.admin_id = str(uuid4())
        self.session_id = str(uuid4())
        
        with self.application.app_context():
            db.create_all()
            user_id_increment = 0
            for i in range(10): # valid users
                user_id_increment += i+1
                user = User(id=user_id_increment, username=f"user{i}", mail=f"user{i}@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=False)
                db.session.add(user)
            for i in range(5): # unverified users
                user_id_increment += i+1
                user = User(id=user_id_increment, username=f"user{i}", mail=f"user{i}@example.com", password="random", passphraseSalt="doesn't matter", isVerified=False, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=False)
                db.session.add(user)
            for i in range(2): # blocked users
                user_id_increment += i+1
                user = User(id=user_id_increment, username=f"user{i}", mail=f"user{i}@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=True)
                db.session.add(user)
            
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

    def test_get_users_per_category(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(self.endpoint)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["total_users"], 17)
            self.assertEqual(response.json()["verified_users"], 12)
            self.assertEqual(response.json()["blocked_users"], 2)
