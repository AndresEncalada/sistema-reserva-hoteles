from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.reserva_model import ReservaModel
from models.habitacion_model import HabitacionModel

class ReservaRepository:
    async def obtener_por_id(self, db: AsyncSession, reserva_id: int):
        result = await db.execute(select(ReservaModel).where(ReservaModel.id == reserva_id))
        return result.scalars().first()

    async def cancelar_reserva(self, db: AsyncSession, reserva_id: int):
        result = await db.execute(select(ReservaModel).where(ReservaModel.id == reserva_id))
        reserva = result.scalars().first()
        
        if reserva:
            reserva.estado = "cancelada"
            
            
            res_hab = await db.execute(
                select(HabitacionModel).where(HabitacionModel.id == reserva.habitacion_id)
            )
            habitacion = res_hab.scalars().first()
            if habitacion:
                habitacion.disponible = True
                
            await db.commit()
            await db.refresh(reserva)
        return reserva

reserva_repo = ReservaRepository()