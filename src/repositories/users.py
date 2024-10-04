from src.schemas.users import User
from src.models.users import UsersModel
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User
