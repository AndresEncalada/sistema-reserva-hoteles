import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

from core.database import AsyncSessionLocal
from models.user_model import UserModel
from models.user_schema import Role
from core.security import get_password_hash

async def seed():
    async with AsyncSessionLocal() as db:
        # Verificamos si ya existe el admin para no duplicarlo
        from sqlalchemy.future import select
        result = await db.execute(select(UserModel).where(UserModel.email == "admin@hotel.com"))
        if result.scalar_one_or_none():
            print("⚠️ Los usuarios de prueba ya existen.")
            return

        # Creamos los usuarios
        admin = UserModel(
            email="admin@hotel.com",
            hashed_password=get_password_hash("admin123"),
            role=Role.ADMIN
        )
        user = UserModel(
            email="huesped@hotel.com",
            hashed_password=get_password_hash("huesped123"),
            role=Role.USER
        )

        db.add_all([admin, user])
        await db.commit()
if __name__ == "__main__":
    asyncio.run(seed())