from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import SessionDep, UserIdDep
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserJwt, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'],)


@router.post('/register')
async def create_user(
    data: UserRequestAdd,
    session: SessionDep
):
    hashed_password = AuthService().pwd_context.hash(data.password)
    modified_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role,
    )
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
async def get_jwt(
    data: UserJwt,
    response: Response,
    session: SessionDep
):
    requested_user = await UsersRepository(session).get_user_by_email(
        email=data.email
    )
    if requested_user is None:
        raise HTTPException(
            status_code=401, detail='Пользователь не найден')

    if not AuthService().verify_password(
        data.password, requested_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail='Неверный пароль')
    access_token = AuthService().create_access_token(
        {'user_id': requested_user.id}
    )
    response.set_cookie("access_token", access_token)
    return {'access_token': access_token}


@router.delete('/logout')
async def delete_jwt(
    response: Response
):
    response.delete_cookie('access_token')
    return {'statuts': 'OK'}


@router.get('/me')
async def get_me(
    user_id: UserIdDep,
    session: SessionDep,
):
    return await UsersRepository(session).get_one_or_none(id=user_id)
