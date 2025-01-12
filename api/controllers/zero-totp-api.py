from flask import request, Response
import os
from main_database.repositories import user as user_repo, google_drive_integration as google_drive_repo, totp_codes as totp_codes_repo
from base64 import b64encode, b64decode
from environment.configuration import conf, logging
import json
import requests


def get_status():
    healthcheck_response = requests.get(f"{conf.zero_totp.api_uri}/healthcheck", verify=not conf.zero_totp.bypass_cert_verification)
    if healthcheck_response.status_code != 200 and healthcheck_response.status_code != 500:
        logging.error(f"Zero-TOTP API is not available. Got status {healthcheck_response.status_code} and response {healthcheck_response.text}")
        return {"error": f"Zero-TOTP API is not available. Got status {healthcheck_response.status_code}. Check the logs to see the full response from the Zero-TOTP API."}, 500
    try:
        healthcheck_data = healthcheck_response.json()
        logging.info(healthcheck_data)
        version = healthcheck_data.get("version")
        healthcheck = healthcheck_data.get("health")
    except:
        logging.error(f"Zero-TOTP API is not available. Got status {healthcheck_response.status_code} and response {healthcheck_response.text}")
        return {"error": f"Zero-TOTP API is not available. Got status {healthcheck_response.status_code}. Check the logs to see the full response from the Zero-TOTP API."}, 500
    return {"version": version, "healthcheck":healthcheck},200

    
