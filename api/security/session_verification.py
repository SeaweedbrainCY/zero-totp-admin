import admin_database.repositories.session as session_repo
from flask import request
from main import app
from connexion.exceptions import OAuthProblem

def verify_session(token_info):
    if not token_info:
        raise OAuthProblem("No authorization token provided")
    with app.app.app_context():
        user_id = session_repo.verify_session(token_info)
    if not user_id:
        print("Invalid authorization token")
        raise OAuthProblem("Invalid authorization token")
    return  {"uid" : user_id}