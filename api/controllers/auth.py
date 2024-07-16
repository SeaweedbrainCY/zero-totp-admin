from flask import request


def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return {"error": "Missing username or password"}, 400
