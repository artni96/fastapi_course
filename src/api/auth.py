from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.config import settings
from src.db import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserJwt, UserRequestAdd


router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'],)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORTIHM
    )
    return encoded_jwt


@router.post('/register')
async def create_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
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


@router.post('/login')
async def get_jwt(data: UserJwt):
    async with async_session_maker() as session:
        requested_user = await UsersRepository(session).get_one_or_none(
            email=data.email
        )
        if requested_user is not None:
            access_token = create_access_token({'user_id': requested_user.id})
            return {'access_token': access_token}
        raise HTTPException(status_code=401, detail='Пользователь не найден')
