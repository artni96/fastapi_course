from fastapi import APIRouter

from src.api.dependencies import UserDep, DBDep
from src.exceptions import (
    EmailNotRegisteredException,
    IncorrectPasswordException,
    UserAlreadyExistsException,
)
from src.schemas.users import UserRequestAdd, UserLoginRequest
from src.services.users import AuthService
from fastapi import HTTPException, status, Response

user_router = APIRouter(tags=['Пользователи',], prefix='/users')

@user_router.post(
    "/register",
    summary='Создание нового пользователя',
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        return await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователь уже зарегистрирован')


@user_router.post(
    "/login",
    summary='Вход пользователя в систему'
)
async def login_user(
    data: UserLoginRequest,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователь с указанной  почтой не '
                                                                            'зарегистрирован')
    except IncorrectPasswordException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный пароль')

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@user_router.get("/me", summary="Мой профиль")
async def get_me(
    user: UserDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none_user(user)


@user_router.post(
    "/logout",
    summary='Выход пользователя из системы',
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
