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
    pass

def create_notification():
    pass