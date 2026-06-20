from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import Role
from controllers.dependencies import get_current_user_token, require_role
from models.habitacion_schema import HabitacionCreate, HabitacionResponse
from services.habitacion_service import habitacion_service

router = APIRouter(prefix="/api/habitaciones", tags=["Habitaciones"])

@router.get("/", response_model=list[HabitacionResponse])
async def listar_habitaciones(
    tipo: Optional[str] = Query(default=None),
    precio_min: Optional[int] = Query(default=None),
    precio_max: Optional[int] = Query(default=None),
    disponible: Optional[bool] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    return await habitacion_service.listar_habitaciones(db, tipo, precio_min, precio_max, disponible)

@router.get("/{id}", response_model=HabitacionResponse)
async def obtener_habitacion(
    id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    habitacion = await habitacion_service.obtener_habitacion(db, id)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion

@router.post("/", response_model=HabitacionResponse, status_code=201)
async def crear_habitacion(
    datos: HabitacionCreate,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    try:
        return await habitacion_service.crear_habitacion(db, datos)
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Ya existe una habitación con el número '{datos.numero}'")

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

@router.delete("/{id}", status_code=204)
async def eliminar_habitacion(
    id: int,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    habitacion = await habitacion_service.eliminar_habitacion(db, id)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")