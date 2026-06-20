from sqlalchemy.ext.asyncio import AsyncSession
from repositories.habitacion_repo import habitacion_repo
from models.habitacion_schema import HabitacionCreate

class HabitacionService:
    async def listar_habitaciones(self, db: AsyncSession):
        return await habitacion_repo.obtener_todas(db)

    async def obtener_habitacion(self, db: AsyncSession, habitacion_id: int):
        return await habitacion_repo.obtener_por_id(db, habitacion_id)

    async def crear_habitacion(self, db: AsyncSession, datos: HabitacionCreate):
        return await habitacion_repo.crear(db, datos)

    async def eliminar_habitacion(self, db: AsyncSession, habitacion_id: int):
        return await habitacion_repo.eliminar(db, habitacion_id)

    async def cambiar_estado(self, db: AsyncSession, habitacion_id: int, estado: bool):
        return await habitacion_repo.cambiar_estado(db, habitacion_id, estado)

habitacion_service = HabitacionService()