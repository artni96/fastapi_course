from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class HotelsModel(Base):

    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
