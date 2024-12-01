from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class BookingModel(Base):
    room_id: Mapped[int] = mapped_column(ForeignKey("roomsmodel.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

    @hybrid_property
    def total_cost(self) -> int:
        return (self.date_to - self.date_from).days * self.price
