from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class FacilitiesMolel(Base):
    title: Mapped[int] = mapped_column(String(64))


class RoomFacilitiesModel(Base):
    room_id: Mapped[int] = mapped_column(ForeignKey('roomsmodel.id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilitiesmolel.id'))
