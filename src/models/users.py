from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(128))
