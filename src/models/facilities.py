from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class FacilitiesMolel(Base):
    title: Mapped[int] = mapped_column(String(64))

    rooms: Mapped[list['RoomsModel']] = relationship(
        back_populates='facilities',
        secondary='roomfacilitiesmodel',
    )


class RoomFacilitiesModel(Base):
    room_id: Mapped[int] = mapped_column(ForeignKey('roomsmodel.id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilitiesmolel.id'))
