from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Annotated
from src.services.auth import AuthService


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
