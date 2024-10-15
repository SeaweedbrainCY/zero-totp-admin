from flask import request, Response
import os
from main_database.repositories import user as user_repo, google_drive_integration as google_drive_repo, totp_codes as totp_codes_repo
from base64 import b64encode, b64decode
from environment.configuration import conf, logging
import json


def get_all_users():
    all_users = user_repo.get_all_users()
    users_info = []
    for user in all_users:
        info, status = get_user_by_id(user.id)
        if status == 200:
            users_info.append(info)
        else:
            logging.error(f"Error getting user info for user {user.id}. Got status {status}")
    return {"users": users_info}, 200


def get_user_by_id(user_id):
    user = user_repo.get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404
    total_totp_secrets = totp_codes_repo.count_totp_secrets_by_user_id(user_id)
    google_drive_enabled = google_drive_repo.is_google_drive_enabled_by_userid(user_id)

    return {
        "username": user.username,
        "email": user.mail,
        "id": user.id, 
        "signup_date": user.createdAt, 
        "isVerified": user.isVerified,
        "isBlocked": user.isBlocked,
        "total_of_2fa": total_totp_secrets,
        "is_google_drive_enabled": google_drive_enabled,
        "last_login_date": int(float(user.last_login_date))
    }, 200

def block_user(user_id):
    user = user_repo.update_blocked_status_by_userid(user_id, is_blocked=True)
    if not user:
        return {"error": "User not found"}, 404
    logging.info(f"User {user_id} blocked")
    return {
       "message": "User blocked successfully"
    }, 201

def unblock_user(user_id):
    user = user_repo.update_blocked_status_by_userid(user_id, is_blocked=False)
    if not user:
        return {"error": "User not found"}, 404
    logging.info(f"User {user_id} unblocked")
    return {
       "message": "User unblocked successfully"
    }, 201


def delete_user(user_id):
    if not conf.features.admin_can_delete:
        return {"error": "Admin cannot delete users. This feature is deactivated for security reasons and can only be enabled in API configuration at startup"}, 403
    user = user_repo.delete_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404
    logging.info(f"User {user_id} deleted")
    return {
       "message": "User deleted successfully"
    }, 201