from sqlalchemy.ext.asyncio import AsyncSession
from repositories.reserva_repo import reserva_repo

class ReservaService:
    async def enviar_notificacion_pago(self, db: AsyncSession, reserva_id: int):
        reserva = await reserva_repo.obtener_por_id(db, reserva_id)
        if not reserva:
            return None
        
        # Aquí conectarías tu servicio de Email, SMS o WhatsApp en el futuro
        # Por ahora, simulamos la acción:
        print(f"[NOTIFICACIÓN] Enviando alerta al cliente {reserva.usuario_id}: 'Tu reserva #{reserva.id} está pendiente de pago.'")
        
        return {"status": "notificado", "mensaje": "Notificación de pago pendiente enviada con éxito"}

    async def cancelar_reserva(self, db: AsyncSession, reserva_id: int):
        return await reserva_repo.cancelar_reserva(db, reserva_id)

reserva_service = ReservaService()