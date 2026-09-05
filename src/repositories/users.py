from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserResponse, UserResponseWithHashPass


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = UserResponse

    async def get_user_with_hash_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return UserResponseWithHashPass.model_validate(orm, from_attributes=True)
