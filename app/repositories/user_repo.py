from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import UserModel

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()