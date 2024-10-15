from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session, async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.models.users import User
from src.services.users import current_user


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_current_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='Не предоставлен токен')
    return token


def get_current_user_id(token: str = Depends(get_current_token)) -> int:
    return AuthService().decode_token(token).get('user_id')


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
UserDep = Annotated[User, Depends(current_user)]
