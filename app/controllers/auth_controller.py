from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import UserLogin, Token
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(
    # Recibimos los datos como un formulario OAuth2 (lo que usa Swagger)
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    
    # Transformamos el 'username' del formulario al 'email' que requiere el sistema original
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    
    # Pasamos las credenciales intactas al servicio original sin modificar su lógica
    return await auth_service.authenticate_user(credentials)