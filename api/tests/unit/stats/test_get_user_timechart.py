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
from freezegun import freeze_time

class TestGetUserTimchart(unittest.TestCase):
    def setUp(self):
        if conf.database.zero_totp_admin_uri != "sqlite:///:memory:" or conf.database.zero_totp_db_uri != "sqlite:///:memory:":
                raise Exception("Test must be run with in memory database")
        self.application = app.app
        self.client = app.test_client()
        self.endpoint = "/api/v1/stats/users/timechart"

        self.admin_id = str(uuid4())
        self.creation_timestamp = dt.datetime.now(dt.UTC).timestamp()
        self.session_id = str(uuid4())
        # today is 2024-07-15
        self.timechart = {
            "2024-07-01": 10,
            "2024-06-01": 7,
            "2024-05-01": 7,
            "2024-04-01": 7,
            "2024-03-01": 7,
            "2024-02-01": 7,
            "2024-01-01": 7,
            "2023-12-01": 6,
            "2023-11-01": 4,
            "2023-10-01": 4,
            "2023-09-01": 4,
            "2023-08-01": 4,
            "2023-07-01": 2,
        }

        creations_date = ["12/05/2022", "01/07/2023", "02/07/2023", "31/07/2023", "15/11/2023", "15/11/2023", "01/01/2024", "15/06/2024", "15/06/2024", "15/06/2024"]
        
        with self.application.app_context():
            db.create_all()
            user_id_increment = 0
            for i in range(len(creations_date)): # valid users
                user_id_increment += i+1
                user = User(id=user_id_increment, username=f"user{i}", mail=f"user{i}@example.com", password="random", passphraseSalt="doesn't matter", isVerified=True, derivedKeySalt="doesn't matter", createdAt=creations_date[i], isBlocked=False)
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


    @freeze_time("2024-07-15")
    def test_get_user_timechart(self):
        with self.application.app_context():
            self.client.cookies = {"session_id": self.session_id}
            response = self.client.get(self.endpoint)
            self.assertEqual(response.status_code, 200)
            for date in self.timechart.keys():
                self.assertEqual(response.json()[date], self.timechart[date])