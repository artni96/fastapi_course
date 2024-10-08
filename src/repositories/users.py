from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import User as UserModel
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserJwtWithHashedPassword


class UsersRepository(BaseRepository):
    model = UserModel
    schema = User

    async def get_user_by_email(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        if model_obj is not None:
            return UserJwtWithHashedPassword.model_validate(
                model_obj
            )
