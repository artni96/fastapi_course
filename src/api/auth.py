from fastapi import APIRouter
from src.schemas.users import UserRequestAdd, UserAdd
from src.db import async_session_maker
from src.repositories.users import UsersRepository
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'],)


@router.post('/register')
async def create_user(data: UserRequestAdd):
    hashed_password = 'hashed_password'
    modified_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role
    )
    async with async_session_maker() as session:
        try:
            new_user = await UsersRepository(session).add(modified_user_data)
            await session.commit()
            return new_user
        except IntegrityError as err:
            if 'Key (username)=(string) already exists' in str(err._message):
                return (
                    f'Пользователь с username "{data.username}" уже существует'
                )
            elif 'Key (email)=(string) already exists' in str(err._message):
                return (
                    f'Пользователь с email "{data.email}" уже существует.'
                )
