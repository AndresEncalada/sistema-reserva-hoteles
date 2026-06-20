import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.reserva_repo import reserva_repo
from repositories.factura_repo import factura_repo
from models.reserva_schema import ReservaCreate

class ReservaService:
    async def crear_reserva(self, db: AsyncSession, datos: ReservaCreate, usuario_id: uuid.UUID):
        return await reserva_repo.crear(db, datos, usuario_id)

    async def listar_reservas(self, db: AsyncSession):
        return await reserva_repo.listar_todas(db)

    async def listar_mis_reservas(self, db: AsyncSession, usuario_id: uuid.UUID):
        return await reserva_repo.listar_por_usuario(db, usuario_id)

    async def marcar_pagado(self, db: AsyncSession, reserva_id: int):
        reserva = await reserva_repo.marcar_pagado(db, reserva_id)
        if reserva and not await factura_repo.obtener_por_reserva(db, reserva_id):
            await factura_repo.crear(db, reserva.id, reserva.usuario_id, reserva.costo_total or 0)
        return reserva

    async def enviar_notificacion_pago(self, db: AsyncSession, reserva_id: int):
        reserva = await reserva_repo.obtener_por_id(db, reserva_id)
        if not reserva:
            return None
        print(f"[NOTIFICACIÓN] Enviando alerta al cliente {reserva.usuario_id}: 'Tu reserva #{reserva.id} está pendiente de pago.'")
        return {"status": "notificado", "mensaje": "Notificación de pago pendiente enviada con éxito"}

    async def cancelar_reserva(self, db: AsyncSession, reserva_id: int):
        return await reserva_repo.cancelar_reserva(db, reserva_id)

reserva_service = ReservaService()