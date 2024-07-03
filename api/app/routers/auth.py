from fastapi import APIRouter
from app.models.auth import AuthModel

router = APIRouter()

@router.post("/auth/login")
def login(body: AuthModel):
    return {"message": "Login"}