from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date, timedelta


class BookingModel(Base):

    room_id: Mapped[int] = mapped_column(ForeignKey('roomsmodel.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return (self.date_to - self.date_from).days * self.price
