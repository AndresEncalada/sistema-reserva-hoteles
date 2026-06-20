import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import UserModel
from models.user_schema import Role

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    async def listar_todos(self) -> list[UserModel]:
        result = await self.db.execute(select(UserModel))
        return result.scalars().all()

    async def create_user(self, email: str, hashed_password: str) -> UserModel:
        user = UserModel(email=email, hashed_password=hashed_password, role=Role.USER)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def cambiar_password(self, user: UserModel, hashed_password: str) -> UserModel:
        user.hashed_password = hashed_password
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def eliminar(self, user: UserModel) -> None:
        await self.db.delete(user)
        await self.db.commit()