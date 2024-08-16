import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import User
from environment.configuration import conf
from admin_database.models import Admin as AdminModel, Session as SessionModel
from main_database.repositories.user import get_user_by_id
from uuid import uuid4
import datetime as dt
import json

class TestBlockUser(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.  zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception(f"Test must be run with in memory database. Admin URI: {conf.database.zero_totp_admin_uri} User URI: {conf.database.zero_totp_db_uri}")
        self.application = app.app
        self.client = app.test_client()
        self.user_id = 1
        self.endpoint = "/api/v1/users/block/"
        self.session_id = str(uuid4())

        with self.application.app_context():
            db.create_all()
            self.user = User(id=self.user_id, username=f"user1", mail=f"user1@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=False)
            db.session.add(self.user)

            admin = AdminModel(id=str(uuid4()), username="root", password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=admin.id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)
            db.session.commit()
    
    def tearDown(self):
        with self.application.app_context():
            db.session.expunge_all()
            db.session.remove()
            db.drop_all()
            patch.stopall()

    

    def test_block_user(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}{self.user_id}")
            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.json()["message"], "User blocked successfully")
            user = get_user_by_id(self.user_id)
            self.assertTrue(user.isBlocked)

    def test_block_user_not_found(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.put(f"{self.endpoint}2")
            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.json()["error"], "User not found")
    
    def test_block_user_already_blocked(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            self.user.isBlocked = True
            db.session.commit()
            response = self.client.put(f"{self.endpoint}{self.user_id}")
            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.json()["message"], "User blocked successfully")
            user = get_user_by_id(self.user_id)
            self.assertTrue(user.isBlocked)
