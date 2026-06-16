from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72) 

class Token(BaseModel):
    access_token: str
    token_type: str