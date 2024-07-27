import tools 
from unittest.mock import patch
import unittest
from unittest.mock import patch
from environment.configuration import conf
from admin_database.models import Admin as AdminModel
from hashlib import scrypt
from base64 import b64encode, b64decode
import tools.regenerate_root_password
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

    

class TestRegenerateRootPassword(unittest.TestCase):
    engine = None 
    def setUp(self):
        self.old_uri = conf.database.zero_totp_admin_uri
        zero_totp_admin_uri = "sqlite:////tmp/test.db"
        self.engine = create_engine(zero_totp_admin_uri)
        with Session(self.engine) as session:
            # create table
            metadata = AdminModel.metadata
            metadata.create_all(self.engine)
            admin = AdminModel(id="1", username="root", password="random", password_salt="doesn't matter")
            session.add(admin)
            session.commit()
            
    def tearDown(self):
        with Session(self.engine) as session:
            metadata = AdminModel.metadata
            metadata.drop_all(self.engine)
            patch.stopall()
        tools.regenerate_root_password.conf.database.zero_totp_admin_uri = self.old_uri
    
    def hash_password(self, password, salt):
        return b64encode(scrypt(password.encode(), salt=salt, n=conf.security.scrypt_n, r=conf.security.scrypt_r, p=conf.security.scrypt_p))

    def test_regenerate_root_password(self):
        self.get_pass_patcher = patch("tools.regenerate_root_password.getpass").start()
        self.get_pass_patcher.return_value = "new_password"
        tools.regenerate_root_password.conf.database.zero_totp_admin_uri = "sqlite:////tmp/test.db"
        with Session(self.engine) as session:
            tools.regenerate_root_password.reset()
            admin = session.query(AdminModel).filter(AdminModel.username == "root").first()
            hashed_password = self.hash_password("new_password", b64decode(admin.password_salt))
            self.assertEqual(admin.password, hashed_password)