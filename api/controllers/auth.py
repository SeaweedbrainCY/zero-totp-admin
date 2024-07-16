from flask import request
from hashlib import scrypt
from admin_database.repositories.admin_repo import get_user_by_username
import os
from base64 import b64encode, b64decode
from environment.configuration import conf

def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return {"error": "Missing username or password"}, 400
    user = get_user_by_username(username)
    if not user:
        #fight against timing attacks
        scrypt(password.encode(), salt=os.urandom(16), n=conf.security.scrypt_n, r=conf.security.scrypt_r, p=conf.security.scrypt_p)
        return {"error": "Invalid username or password"}, 403
    else:
        salt = b64decode(user.password_salt)
        hashed_pass = b64encode(scrypt(password.encode(), salt=salt, n=conf.security.scrypt_n, r=conf.security.scrypt_r, p=conf.security.scrypt_p))
        print(hashed_pass)
        print(user.password)
        if hashed_pass != user.password:
            return {"error": "Invalid username or password"}, 403
        else:
            return {"message": "Login successful"}, 200
