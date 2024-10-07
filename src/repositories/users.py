from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersModel
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserJwtWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def get_one_or_none(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        if model_obj is not None:
            return UserJwtWithHashedPassword.model_validate(
                model_obj
            )
