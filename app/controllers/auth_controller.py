from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import UserLogin, UserCreate, Token
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.authenticate_user(credentials)

@router.post("/registro", response_model=Token, status_code=201)
async def registro(
    datos: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.register_user(datos)