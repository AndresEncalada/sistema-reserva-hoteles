from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import Role
from controllers.dependencies import get_current_user_token, require_role
from models.habitacion_schema import HabitacionResponse
from services.habitacion_service import habitacion_service

router = APIRouter(prefix="/api/habitaciones", tags=["Habitaciones"])

# ENDPOINT 1: Listar habitaciones Cliente
@router.get("/", response_model=list[HabitacionResponse])
async def listar_habitaciones(
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    return await habitacion_service.listar_habitaciones(db)

#ENDPOINT 2: Cambiar estado Solo Admin
@router.patch("/{id}/estado", response_model=HabitacionResponse)
async def cambiar_estado(
    id: int,
    disponible: bool,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    habitacion = await habitacion_service.cambiar_estado(db, id, disponible)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion