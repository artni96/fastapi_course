from fastapi import APIRouter

from services.users import auth_backend, fastapi_users
from src.schemas.users import UserCreate, UserRead, UserUpdate


user_router = APIRouter(prefix='/auth')


user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Авторизация и аутентификация'],
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Авторизация и аутентификация'],
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['Пользователи'],
)
