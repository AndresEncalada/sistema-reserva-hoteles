# app/controllers/reserva_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from controllers.dependencies import get_current_user_token
from models.reserva_schema import ReservaResponse
from services.reserva_service import reserva_service

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

# ENDPOINT: Notificación de pago pendiente
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

# ENDPOINT: Cancelar una reserva
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