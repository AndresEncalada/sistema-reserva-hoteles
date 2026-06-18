import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

from core.database import engine, Base
# Importamos los modelos para que SQLAlchemy sepa qué tablas crear
from models.user_model import UserModel 
from models.habitacion_model import HabitacionModel
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())