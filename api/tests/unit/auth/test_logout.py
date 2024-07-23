import unittest
from main import app,db
from unittest.mock import patch
from environment.configuration import conf
from admin_database.models import Admin as AdminModel, Session as SessionModel
from admin_database.repositories import session as session_repo
from uuid import uuid4
import datetime as dt


class TestLogin(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception("Test must be run with in memory database")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/logout"

        self.admin_id = str(uuid4())
        self.admin_username = "root"
        self.session_id = str(uuid4())
        
        with self.application.app_context():
            db.create_all()
            admin = AdminModel(id=self.admin_id, username=self.admin_username, password="random", password_salt="doesn't matter")
            session = SessionModel(id=self.session_id, user_id=self.admin_id, expiration=dt.datetime.now(dt.UTC).timestamp() + 3600)
            db.session.add(admin)
            db.session.add(session)
            db.session.commit()
    

    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
            patch.stopall()
    
    def test_logout(self):
         with self.application.app_context():
              self.client.cookies = {"session_id": self.session_id}
              response = self.client.post(self.endpoint)
              self.assertEqual(response.status_code, 200)
              self.assertIsNone(db.session.query(SessionModel).filter_by(id=self.session_id).first())
    
    
