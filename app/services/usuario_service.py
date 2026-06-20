import uuid
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repo import UserRepository
from core.security import verify_password, get_password_hash
from models.user_schema import PasswordChange

class UsuarioService:
    async def obtener_perfil(self, db: AsyncSession, email: str):
        repo = UserRepository(db)
        return await repo.get_user_by_email(email)

    async def cambiar_password(self, db: AsyncSession, email: str, datos: PasswordChange):
        repo = UserRepository(db)
        user = await repo.get_user_by_email(email)
        if not user or not verify_password(datos.password_actual, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual es incorrecta",
            )
        hashed = get_password_hash(datos.password_nuevo)
        return await repo.cambiar_password(user, hashed)

    async def listar_usuarios(self, db: AsyncSession):
        repo = UserRepository(db)
        return await repo.listar_todos()

    async def eliminar_usuario(self, db: AsyncSession, user_id: uuid.UUID, email_admin: str):
        repo = UserRepository(db)
        user = await repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if user.email == email_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar tu propia cuenta",
            )
        try:
            await repo.eliminar(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el usuario porque tiene reservas asociadas",
            )

usuario_service = UsuarioService()
