import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import UserResponse, PasswordChange, Role
from controllers.dependencies import get_current_user_token, require_role
from services.usuario_service import usuario_service

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/me", response_model=UserResponse)
async def obtener_perfil(
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    user = await usuario_service.obtener_perfil(db, usuario_actual["email"])
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.patch("/me/password")
async def cambiar_password(
    datos: PasswordChange,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    await usuario_service.cambiar_password(db, usuario_actual["email"], datos)
    return {"mensaje": "Contraseña actualizada correctamente"}

@router.get("/", response_model=list[UserResponse])
async def listar_usuarios(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    return await usuario_service.listar_usuarios(db)

@router.delete("/{id}", status_code=204)
async def eliminar_usuario(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    await usuario_service.eliminar_usuario(db, id, admin["email"])
