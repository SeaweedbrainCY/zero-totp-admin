from fastapi import APIRouter
from zero_totp_db_model.model import User
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/stats/users")
def login(db:Session):
    return db.query(User).first()