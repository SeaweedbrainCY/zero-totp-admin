from flask import request, Response
import os
from main_database.repositories import notifications as notif_repo
from base64 import b64encode, b64decode
from environment.configuration import conf, logging
import json
import datetime as dt

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
    notif = notif_repo.get_notification_by_id(notif_id)
    if not notif:
        return {"error": "Notification not found"}, 404
    message = request.json.get("message") if request.json.get("message") is not None else notif.message
    expiry = request.json.get("expiration_timestamp_utc") if request.json.get("expiration_timestamp_utc") is not None else notif.expiry
    enabled = request.json.get("enabled") if request.json.get("enabled") is not None else notif.enabled
    authenticated_user_only = request.json.get("auth_user_only") if request.json.get("auth_user_only") is not None else notif.authenticated_user_only
    print("expiry", expiry)
    if expiry:
        try:
            if int(float(expiry)) < dt.datetime.now().timestamp():
                return {"error": "Expiration date must be in the future"}, 400
            if int(float(expiry)) > (dt.datetime.now() + dt.timedelta(days=365*5)).timestamp(): 
                return {"error": "Expiration date cannot be more than 5 years in the future. Set expiration to None to keep a notification indefinitely."}, 400
        except ValueError as e:
            logging.error(f"Invalid expiration date format. UNIX timestamp expected. {e}")
            return {"error": "Invalid expiration date format. UNIX timestamp expected"}, 400
    if message == "":
        return {"error": "Message cannot be empty"}, 400    
    if len(message) > 765:
        return {"error": "Message cannot be longer than 765 characters"}, 400
    notif = notif_repo.update_notification(notif_id, message, expiry, enabled, authenticated_user_only)
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

def delete_notification(notif_id):
    notif = notif_repo.get_notification_by_id(notif_id)
    if not notif:
        return {"error": "Notification not found"}, 404
    if notif_repo.delete_notification(notif_id):
        return {"message": "Success"}, 200
    logging.error(f"Internal server error. Impossible to delete notification {notif_id}. notif_repo.delete_notification returned False")
    return {"error": "Internal server error"}, 500

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
    if expiry :
        try:
            if int(float(expiry))  < dt.datetime.now().timestamp():
                return {"error": "Expiration date must be in the future"}, 400
            if int(float(expiry))  > (dt.datetime.now() + dt.timedelta(days=365*5)).timestamp(): 
                return {"error": "Expiration date cannot be more than 5 years in the future. Set expiration to None to keep a notification indefinitely."}, 400
        except ValueError:
            return {"error": "Invalid expiration date format. UNIX timestamp expected"}, 400
    if message == "":
        return {"error": "Message cannot be empty"}, 400    
    if len(message) > 765:
        return {"error": "Message cannot be longer than 765 characters"}, 400
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

    

