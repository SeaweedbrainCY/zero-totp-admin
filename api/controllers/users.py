from flask import request, Response
import os
from main_database.repositories import user as user_repo
from base64 import b64encode, b64decode
from environment.configuration import conf
import json


def get_all_users():
    pass

def get_user(user_id):
    user = user_repo.get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404

    return {
        "username": user.username,
        "email": user.mail,
        "id": user.id, 
        "signup_date": user.createdAt, 
        "isVerified": user.isVerified,
        "isBlocked": user.isBlocked
    }