from flask_sqlalchemy import SQLAlchemy
from ..models import Session
from main import db
import datetime
from uuid import uuid4
from environment.configuration import logging, conf


def delete_session(session_id) -> None:
    session = db.session.query(Session).filter(Session.id == session_id).first()
    db.session.delete(session)
    db.session.commit()

def verify_session(session_id) -> str: # return user_id if session is valid, else return None
    session = db.session.query(Session).filter(Session.id == session_id).first()
    if not session:
        return None
    if datetime.datetime.now(datetime.UTC).timestamp() > session.expiration:
        delete_session(session_id)
        return None
    return session.user_id

def create_session(user_id) -> str:
    try:
        expiration = datetime.datetime.now(datetime.UTC).timestamp() + conf.api.session_ttl # 2 hour 
        session = Session(id=str(uuid4()), user_id=user_id, expiration=expiration)
        db.session.add(session)
        db.session.commit()
        return session.id
    except Exception as e:
        logging.error(f"Failed to create session. Error: {e}")
        return None