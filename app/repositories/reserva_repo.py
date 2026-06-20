import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.reserva_model import ReservaModel
from models.habitacion_model import HabitacionModel
from models.reserva_schema import ReservaCreate

class ReservaRepository:
    async def obtener_por_id(self, db: AsyncSession, reserva_id: int):
        result = await db.execute(select(ReservaModel).where(ReservaModel.id == reserva_id))
        return result.scalars().first()

    async def listar_todas(self, db: AsyncSession):
        result = await db.execute(select(ReservaModel))
        return result.scalars().all()

    async def listar_por_usuario(self, db: AsyncSession, usuario_id: uuid.UUID):
        result = await db.execute(select(ReservaModel).where(ReservaModel.usuario_id == usuario_id))
        return result.scalars().all()

    async def crear(self, db: AsyncSession, datos: ReservaCreate, usuario_id: uuid.UUID):
        res_hab = await db.execute(select(HabitacionModel).where(HabitacionModel.id == datos.habitacion_id))
        habitacion = res_hab.scalars().first()
        if not habitacion or not habitacion.disponible:
            return None

        reserva = ReservaModel(
            usuario_id=usuario_id,
            habitacion_id=datos.habitacion_id,
            estado="pendiente"
        )
        habitacion.disponible = False
        db.add(reserva)
        await db.commit()
        await db.refresh(reserva)
        return reserva

    async def marcar_pagado(self, db: AsyncSession, reserva_id: int):
        result = await db.execute(select(ReservaModel).where(ReservaModel.id == reserva_id))
        reserva = result.scalars().first()
        if reserva:
            reserva.estado = "pagado"
            await db.commit()
            await db.refresh(reserva)
        return reserva

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