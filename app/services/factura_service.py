import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.factura_repo import factura_repo

class FacturaService:
    async def obtener_por_reserva(self, db: AsyncSession, reserva_id: int):
        return await factura_repo.obtener_por_reserva(db, reserva_id)

    async def listar_todas(self, db: AsyncSession):
        return await factura_repo.listar_todas(db)

    async def crear(self, db: AsyncSession, reserva_id: int, usuario_id: uuid.UUID, monto: int):
        return await factura_repo.crear(db, reserva_id, usuario_id, monto)

factura_service = FacturaService()
