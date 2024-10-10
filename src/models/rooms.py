from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import ForeignKey, Column, Integer, CheckConstraint


class RoomsModel(Base):

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotelsmodel.id'))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    # price: Mapped[int] = Column(
    #     Integer, CheckConstraint('price > 0')
    # )
    # quantity: Mapped[int] = Column(
    #     Integer, CheckConstraint('quantity > 0')
    # )

    @validates('price')
    def validate_price(self, key, value: int):
        if value < 0:
            raise ValueError('Значение поля "price" должно быть больше 0!')
        return value

    @validates('quantity')
    def validate_quantity(self, key, value: int):
        if value < 0:
            raise ValueError('Значение поля "quantity" должно быть больше 0!')
        return value
