import uuid
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.factura_model import FacturaModel

class FacturaRepository:
    async def crear(self, db: AsyncSession, reserva_id: int, usuario_id: uuid.UUID, monto: int) -> FacturaModel:
        factura = FacturaModel(
            reserva_id=reserva_id,
            usuario_id=usuario_id,
            monto=monto,
            fecha_emision=date.today(),
        )
        db.add(factura)
        await db.commit()
        await db.refresh(factura)
        return factura

    async def obtener_por_reserva(self, db: AsyncSession, reserva_id: int) -> FacturaModel | None:
        result = await db.execute(select(FacturaModel).where(FacturaModel.reserva_id == reserva_id))
        return result.scalars().first()

    async def listar_todas(self, db: AsyncSession):
        result = await db.execute(select(FacturaModel))
        return result.scalars().all()

factura_repo = FacturaRepository()
