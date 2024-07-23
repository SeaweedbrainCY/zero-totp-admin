from flask import request, Response
from hashlib import scrypt
from admin_database.repositories import admin_repo
from admin_database.repositories import session as session_repo
import os
from base64 import b64encode, b64decode
from environment.configuration import conf
import json

def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = admin_repo.get_user_by_username(username)
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
            session_id = session_repo.create_session(user.id)
            if not session_id:
                return {"error": "Internal server error"}, 500
            response = Response(status=200, mimetype="application/json", response=json.dumps({"status":"OK"}))
            response.set_cookie("session_id", session_id, httponly=True, secure=True, samesite="strict", max_age=conf.api.session_ttl)
            return response

def whoami(user):
    user_obj = admin_repo.get_user_by_id(user)
    if not user_obj:
        return {"error": "User not found"}, 401
    
    return {"username": user_obj.username}, 200

def logout(user):
    cookie = request.cookies.get("session_id")
    session_repo.delete_session(cookie)
    response = Response(status=200, mimetype="application/json", response=json.dumps({"status":"OK"}))
    response.delete_cookie("session_id")
    return response
