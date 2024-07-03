from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/login")
def login():
    return {"message": "Login"}