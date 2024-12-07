from typing import Annotated

from fastapi import Depends, Query, Request, HTTPException, status
from pydantic import BaseModel

from src.services.users import AuthService
from src.db import async_session_maker
from src.exceptions import IncorrectTokenException
from src.models.users import User
from src.schemas.users import UserForJWT
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return token


def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный JWT Token')
        # raise IncorrectTokenHTTPException
    return UserForJWT.model_validate(data, from_attributes=True)
    # return data["user_id"]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
UserDep = Annotated[User, Depends(get_current_user_id)]
