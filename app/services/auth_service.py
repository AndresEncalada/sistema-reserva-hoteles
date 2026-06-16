from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repo import UserRepository
from core.security import verify_password, create_access_token
from models.user_schema import UserLogin, Token
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def authenticate_user(self, credentials: UserLogin) -> Token:
        user = await self.repo.get_user_by_email(credentials.email)
        
        # user ahora es un objeto de SQLAlchemy (UserModel)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role.value}
        )
        return Token(access_token=access_token, token_type="bearer")