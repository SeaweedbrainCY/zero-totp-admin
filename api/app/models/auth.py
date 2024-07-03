from pydantic import BaseModel
from typing import Annotated

class AuthModel(BaseModel):
    username: str
    password: str