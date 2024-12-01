from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from src.db import async_session_maker
from src.models.users import User
from src.services.users import current_user
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
UserDep = Annotated[User, Depends(current_user)]
