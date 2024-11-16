from sqlalchemy import ForeignKey
from sqlalchemy.orm import (Mapped, mapped_column, relationship,
                            validates)
from src.db import Base


class RoomsModel(Base):

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotelsmodel.id'))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list['FacilitiesMolel'] | None] = relationship(
        back_populates='rooms',
        secondary='roomfacilitiesmodel'
    )

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
