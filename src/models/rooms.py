from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class RoomsModel(Base):

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotelsmodel.id'))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
