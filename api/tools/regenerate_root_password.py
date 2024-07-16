from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from environment.configuration import conf
from admin_database.models import Admin
import os
from hashlib import scrypt
from base64 import b64encode
from uuid import uuid4


print("########################")
print("Regenerate root password")
print("########################\n")
password = getpass(prompt="New root password: ")
confirm_password = getpass(prompt="Confirm new root password: ")
salt = os.urandom(16)
hased_pass = b64encode(scrypt(password.encode(), salt=salt, n=conf.security.scrypt_n, r=conf.security.
scrypt_r, p=conf.security.scrypt_p))
salt_b64 = b64encode(salt)
if password != confirm_password:
    print("Passwords do not match")
    exit(1)


engine = create_engine(conf.database.zero_totp_admin_uri)
with Session(engine) as session:
    admin = session.query(Admin).filter(Admin.username == "root").first()
    if admin:
        admin.password = hased_pass
        admin.password_salt = salt_b64
        session.commit()
    else:
        admin = Admin(id=str(uuid4()), username="root", password=hased_pass, password_salt=salt_b64)
        session.add(admin)
        session.commit()

print("Root password updated successfully")
print("Thanks for using Zero-TOTP!")
