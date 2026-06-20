import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

from core.database import engine, Base
from models.user_model import UserModel
from models.habitacion_model import HabitacionModel
from models.reserva_model import ReservaModel
from models.factura_model import FacturaModel
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())