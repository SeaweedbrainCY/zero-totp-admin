from flask import request, Response
import os
from main_database.repositories import user as user_repo
from base64 import b64encode, b64decode
from environment.configuration import conf, logging
import json


def get_all_users():
    all_users = user_repo.get_all_users()
    users_info = []
    for user in all_users:
        info, status = get_user(user.id)
        if status == 200:
            users_info.append(info)
        else:
            logging.error(f"Error getting user info for user {user.id}. Got status {status}")
    return {"users": users_info}, 200


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
    }, 200