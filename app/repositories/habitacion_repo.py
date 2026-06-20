from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.habitacion_model import HabitacionModel
from models.habitacion_schema import HabitacionCreate

class HabitacionRepository:
    async def obtener_todas(self, db: AsyncSession):
        result = await db.execute(select(HabitacionModel))
        return result.scalars().all()

    async def obtener_por_id(self, db: AsyncSession, habitacion_id: int):
        result = await db.execute(select(HabitacionModel).where(HabitacionModel.id == habitacion_id))
        return result.scalars().first()

    async def crear(self, db: AsyncSession, datos: HabitacionCreate):
        habitacion = HabitacionModel(**datos.model_dump())
        db.add(habitacion)
        await db.commit()
        await db.refresh(habitacion)
        return habitacion

    async def eliminar(self, db: AsyncSession, habitacion_id: int):
        result = await db.execute(select(HabitacionModel).where(HabitacionModel.id == habitacion_id))
        habitacion = result.scalars().first()
        if habitacion:
            await db.delete(habitacion)
            await db.commit()
        return habitacion

    async def cambiar_estado(self, db: AsyncSession, habitacion_id: int, estado: bool):
        result = await db.execute(select(HabitacionModel).where(HabitacionModel.id == habitacion_id))
        habitacion = result.scalars().first()
        if habitacion:
            habitacion.disponible = estado
            await db.commit()
            await db.refresh(habitacion)
        return habitacion

habitacion_repo = HabitacionRepository()