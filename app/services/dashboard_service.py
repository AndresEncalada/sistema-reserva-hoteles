from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.reserva_model import ReservaModel
from models.habitacion_model import HabitacionModel

class DashboardService:
    async def obtener_estadisticas(self, db: AsyncSession) -> dict:
        total_reservas = await db.scalar(select(func.count()).select_from(ReservaModel))

        reservas_pendientes = await db.scalar(
            select(func.count()).select_from(ReservaModel).where(ReservaModel.estado == "pendiente")
        )
        reservas_pagadas = await db.scalar(
            select(func.count()).select_from(ReservaModel).where(ReservaModel.estado == "pagado")
        )
        reservas_canceladas = await db.scalar(
            select(func.count()).select_from(ReservaModel).where(ReservaModel.estado == "cancelada")
        )

        habitaciones_disponibles = await db.scalar(
            select(func.count()).select_from(HabitacionModel).where(HabitacionModel.disponible == True)
        )
        habitaciones_ocupadas = await db.scalar(
            select(func.count()).select_from(HabitacionModel).where(HabitacionModel.disponible == False)
        )

        ingresos_resultado = await db.execute(
            select(func.sum(HabitacionModel.precio))
            .join(ReservaModel, ReservaModel.habitacion_id == HabitacionModel.id)
            .where(ReservaModel.estado == "pagado")
        )
        ingresos_totales = ingresos_resultado.scalar() or 0

        return {
            "reservas": {
                "total": total_reservas,
                "pendientes": reservas_pendientes,
                "pagadas": reservas_pagadas,
                "canceladas": reservas_canceladas,
            },
            "habitaciones": {
                "disponibles": habitaciones_disponibles,
                "ocupadas": habitaciones_ocupadas,
            },
            "ingresos_totales": ingresos_totales,
        }

dashboard_service = DashboardService()
