from fastapi import APIRouter
#
# from src.schemas.users import UserCreate, UserRead, UserUpdate
# from src.services.users import auth_backend, fastapi_users
#
#
# user_router = APIRouter()
#
#
# user_router.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["Авторизация и аутентификация"],
# )
# user_router.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Авторизация и аутентификация"],
# )
# users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
#
# users_router.routes = [
#     rout for rout in users_router.routes if rout.name != "users:delete_user"
# ]  # удаление ручки для удаления пользователя
#
# user_router.include_router(
#     users_router,
#     prefix="/users",
#     tags=["Пользователи"],
# )
#
# route_desired_content = [
#     [
#         "auth:jwt.login",
#         "User login to get access to to protected endpoints",
#         "Вход пользователя в систему",
#     ],
#     ["auth:jwt.logout", "User logout", "Выход из системы"],
#     [
#         "register:register",
#         "Создание нового пользователя в базе данных",
#         "Создание нового пользователя",
#     ],
#     [
#         "users:user",
#         "Gets information from the database about a specific user by id",
#         'Получение информации о пользователе по его "id"',
#     ],
#     [
#         "users:current_user",
#         "Gets information from the database about a specific user by id",
#         "Получение информации об авторизованном пользователе",
#     ],
#     [
#         "users:patch_user",
#         "Changes all information in the database from a specific user by id",
#         'Частичное обновление данных о пользователе по его "id"',
#     ],
#     [
#         "users:patch_current_user",
#         "Changes all information in the database from a specific user by id",
#         "Частичное обновление данных об авторизованном пользователе",
#     ],
# ]
#
# for x in range(0, len(route_desired_content)):
#     route_name = user_router.routes[x].name
#     for z in route_desired_content:
#         if route_name == z[0]:
#             user_router.routes[x].description = z[1]
#             user_router.routes[x].name = z[2]
#

from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import jwt

from src.api.dependencies import UserDep, DBDep
from src.config import settings
from src.exceptions import (
    IncorrectTokenException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
)
from src.schemas.users import UserRequestAdd, UserAdd, UserLoginRequest
from src.services.base import BaseService
from src.services.users import AuthService
from fastapi import HTTPException, status, Response

user_router = APIRouter()

@user_router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return {"status": "OK"}


@user_router.post("/login")
async def login_user(
    data: UserLoginRequest,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        # raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        # raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@user_router.get("/me", summary="Мой профиль")
async def get_me(
    user_id: UserDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none_user(user_id)


@user_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
