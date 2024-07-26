import unittest
from main import app,db
from unittest.mock import patch
from zero_totp_db_model.model import User, RateLimiting
from environment.configuration import conf
from admin_database.models import Admin as AdminModel, Session as SessionModel
from admin_database.repositories import session as session_repo
from uuid import uuid4
import datetime as dt
import json

class TestGetRateLimiting(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception("Test must be run with in memory database")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/stats/server/rate-limiting"

        self.admin_id = str(uuid4())
        self.creation_timestamp = dt.datetime.now(dt.UTC).timestamp()
        self.session_id = str(uuid4())
        self.rate_limited_ip_1 = "1.1.1.1"
        self.rate_limited_ip_2 = "2.2.2.2"
        self.rate_limiting_stats = {
              "rate_limited_ip": 2,
            "rate_limited_emails": 1,
        }
        
        with self.application.app_context():
            db.create_all()
            self.user_ok = User(id=1, username=f"user1", mail=f"user1@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=False)
            self.user_rate_limited = User(id=2, username=f"user3", mail=f"user3@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt="date", isBlocked=False)
            db.session.add(self.user_ok)
            db.session.add(self.user_rate_limited)


            rate_limiting_1 = RateLimiting(id=1, ip=self.rate_limited_ip_1, user_id=None, action_type="failed_login", timestamp=dt.datetime.now(dt.UTC))
            rate_limiting_2 = RateLimiting(id=2, ip=self.rate_limited_ip_2, user_id=2, action_type="failed_login", timestamp=dt.datetime.now(dt.UTC))
            db.session.add(rate_limiting_1)
            db.session.add(rate_limiting_2)

            email_rate_limiting = RateLimiting(id=3, ip=None, user_id=None, action_type="send_verification_email", timestamp=dt.datetime.now(dt.UTC))
            db.session.add(email_rate_limiting)

            
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


    def test_rate_limiting_stats(self):
       with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(self.endpoint)
            self.assertEqual(response.status_code, 200)
            for stat in self.rate_limiting_stats.keys():
                self.assertEqual(response.json()[stat], self.rate_limiting_stats[stat])