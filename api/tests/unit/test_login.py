import unittest
from main import app,db
from unittest.mock import patch
from environment.configuration import conf
from admin_database.models import Admin as AdminModel
from admin_database.repositories import session as session_repo
from uuid import uuid4
import os
from hashlib import scrypt
from base64 import b64encode


class TestLogin(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception("Test must be run with in memory database")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/login"

        self.admin_id = str(uuid4())
        self.admin_username = "root"
        self.admin_password = "password"
        salt = os.urandom(16)
        hashed_pass = b64encode(scrypt(self.admin_password.encode(), salt=salt, n=conf.security.scrypt_n, r=conf.security.
scrypt_r, p=conf.security.scrypt_p))
        salt_b64 = b64encode(salt)

        with self.application.app_context():
            admin = AdminModel(id=self.admin_id, username=self.admin_username, password=hashed_pass, password_salt=salt_b64)
            db.session.add(admin)
            db.session.commit()
    

    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()
    

    def test_login_success(self):
         with self.application.app_context():
            response = self.client.post(self.endpoint, json={"username": self.admin_username, "password": self.admin_password})
            self.assertEqual(response.status_code, 200)
            self.assertIn("session_id", response.headers["Set-Cookie"])
            self.assertIn("HttpOnly", response.headers["Set-Cookie"])
            self.assertIn("Secure", response.headers["Set-Cookie"])
            self.assertIn("SameSite=Strict", response.headers["Set-Cookie"])
            self.assertIn("Expires", response.headers["Set-Cookie"])
            session_id = response.headers["Set-Cookie"].strip().split("session_id=")[1].split(";")[0]
            self.assertTrue(session_repo.verify_session(session_id))

         


