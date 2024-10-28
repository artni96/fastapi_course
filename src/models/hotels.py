from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class HotelsModel(Base):

    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
