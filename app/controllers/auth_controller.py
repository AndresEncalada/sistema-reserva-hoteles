from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from models.user_schema import UserLogin, Token
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.authenticate_user(credentials)