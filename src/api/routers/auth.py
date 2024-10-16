from fastapi import APIRouter

from src.services.users import auth_backend, fastapi_users
from src.schemas.users import UserCreate, UserRead, UserUpdate


user_router = APIRouter()


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
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]  # удалили ручку для удаления пользователя

user_router.include_router(
    users_router,
    prefix='/users',
    tags=['Пользователи'],
)
