from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import Role
from controllers.dependencies import get_current_user_token, require_role
from models.reserva_schema import ReservaCreate, ReservaResponse
from repositories.user_repo import UserRepository
from services.reserva_service import reserva_service

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

@router.post("/", response_model=ReservaResponse, status_code=201)
async def crear_reserva(
    datos: ReservaCreate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(usuario_actual["email"])
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    reserva = await reserva_service.crear_reserva(db, datos, user.id)
    if not reserva:
        raise HTTPException(status_code=400, detail="Habitación no disponible o no existe")
    return reserva

@router.get("/", response_model=list[ReservaResponse])
async def listar_reservas(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    return await reserva_service.listar_reservas(db)

@router.get("/mis-reservas", response_model=list[ReservaResponse])
async def listar_mis_reservas(
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(usuario_actual["email"])
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return await reserva_service.listar_mis_reservas(db, user.id)

@router.patch("/{id}/pagar", response_model=ReservaResponse)
async def marcar_pagado(
    id: int,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    reserva = await reserva_service.marcar_pagado(db, id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.post("/{id}/notificar-pago")
async def notificar_pago(
    id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    resultado = await reserva_service.enviar_notificacion_pago(db, id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return resultado

@router.patch("/{id}/cancelar", response_model=ReservaResponse)
async def cancelar_reserva(
    id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    reserva = await reserva_service.cancelar_reserva(db, id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva
