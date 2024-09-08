from flask import request, Response
import os
from main_database.repositories import notifications as notif_repo
from base64 import b64encode, b64decode
from environment.configuration import conf, logging
import json

def get_notification_by_id(notif_id):
    notif = notif_repo.get_notification_by_id(notif_id)  
    if not notif:
        return {"error": "Notification not found"}, 404
    return {
        "id": notif.id,
        "message": notif.message,
        "timestamp": notif.timestamp,
        "expiration_timestamp": notif.expiry,
        "enabled": notif.enabled,
        "auth_user_only": notif. authenticated_user_only
    }, 200
    

def update_notification(notif_id):
    pass

def delete_notification(notif_id):
    pass

def get_all_notifications():
    notifs = notif_repo.get_all_notifications()
    if not notifs:
        return{"error": "Notifications not found"}, 404
    body = {"notifications": []}
    for notif in notifs:
        body["notifications"].append({
            "id": notif.id,
            "message": notif.message,
            "timestamp": notif.timestamp,
            "expiration_timestamp": notif.expiry,
            "enabled": notif.enabled,
            "auth_user_only": notif. authenticated_user_only
        })
    return body, 200
    

def create_notification():
    message = request.json.get("message")
    expiry = request.json.get("expiration_timestamp_utc") if request.json.get("expiration_timestamp_utc") else None
    enabled = request.json.get("enabled") if request.json.get("enabled") else False 
    authenticated_user_only = request.json.get("auth_user_only") if request.json.get("auth_user_only") else False

    notif = notif_repo.create_notification(message, expiry, enabled, authenticated_user_only)
    if not notif:
        return {"error": "Internal server error"}, 500
    return {
        "id": notif.id,
        "message": notif.message,
        "timestamp": notif.timestamp,
        "expiration_timestamp": notif.expiry,
        "enabled": notif.enabled,
        "auth_user_only": notif. authenticated_user_only
    }, 201

    

