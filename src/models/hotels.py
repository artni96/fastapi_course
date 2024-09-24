from src.db import BaseORM
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class HotelsModel(BaseORM):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
