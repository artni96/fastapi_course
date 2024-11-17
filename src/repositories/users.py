from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import User as UserModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserMapper
from src.schemas.users import User, UserJwtWithHashedPassword


class UsersRepository(BaseRepository):
    model = UserModel
    schema = User
    mapper = UserMapper

    async def get_all(self):
        query = select(
            self.model.email,
            self.model.username,
            self.model.id,
            self.model.first_name,
            self.model.last_name,
    )
        result = await self.session.execute(query)
        result = result.mappings().all()
        return [UserMapper.map_to_domain_entity(obj) for obj in result]

    async def get_user_by_email(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        if model_obj is not None:
            return UserJwtWithHashedPassword.model_validate(
                model_obj
            )
