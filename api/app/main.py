from fastapi import Depends, FastAPI
from database.database import SessionLocal, engine, Base,db
from .routers import auth
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth.router)

def get_db():
    try:
        yield db
    finally:
        db.close()