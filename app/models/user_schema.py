from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import Enum
from uuid import UUID

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: Role
    model_config = ConfigDict(from_attributes=True)

class PasswordChange(BaseModel):
    password_actual: str
    password_nuevo: str = Field(..., min_length=6, max_length=72)

class Token(BaseModel):
    access_token: str
    token_type: str