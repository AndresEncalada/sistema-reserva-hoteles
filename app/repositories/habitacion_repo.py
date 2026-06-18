from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.habitacion_model import HabitacionModel

class HabitacionRepository:
    async def obtener_todas(self, db: AsyncSession):
        # Busca todas las habitaciones
        result = await db.execute(select(HabitacionModel))
        return result.scalars().all()

    async def cambiar_estado(self, db: AsyncSession, habitacion_id: int, estado: bool):
        # Busca una habitación por ID y le cambia la disponibilidad
        result = await db.execute(select(HabitacionModel).where(HabitacionModel.id == habitacion_id))
        habitacion = result.scalars().first()
        
        if habitacion:
            habitacion.disponible = estado
            await db.commit()
            await db.refresh(habitacion)
        return habitacion

habitacion_repo = HabitacionRepository()