from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import ForeignKey, Column, Integer, CheckConstraint


class RoomsModel(Base):

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotelsmodel.id'))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    @validates('price')
    def validate_price(self, key, value: int):
        if value < 0:
            raise ValueError('Значение "price" должно быть больше нуля!')
        return value
