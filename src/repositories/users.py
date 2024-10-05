from sqlalchemy import select
from src.schemas.users import User
from src.models.users import UsersModel
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def get_one_or_none(self, email):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        if result is not None:
            return self.schema.model_validate(
                model_obj, from_attributes=True
            )
        return {'status': 'NOT FOUND'}