from sqlalchemy.ext.asyncio import AsyncSession
from repositories.habitacion_repo import habitacion_repo

class HabitacionService:
    async def listar_habitaciones(self, db: AsyncSession):
        return await habitacion_repo.obtener_todas(db)

    async def cambiar_estado(self, db: AsyncSession, habitacion_id: int, estado: bool):
        return await habitacion_repo.cambiar_estado(db, habitacion_id, estado)

habitacion_service = HabitacionService()