from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomInfo
from sqlalchemy import select, func
from src.db import engine


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomInfo


    """with bookings as (
        select room_id, count(*) as booked_rooms from bookingmodel where date_from >= '2024-10-17' and date_to <= '2024-10-22' group by room_id
    ),
    rooms as (
        select id, quantity, coalesce(booked_rooms, 0), quantity - coalesce(booked_rooms, 0) as avaliable_rooms from roomsmodel
        left join bookings on bookings.room_id = roomsmodel.id
    )
    select * from rooms"""

    async def add(self, date_from, date_to, hotel_id):
        bookings = (
            select(
                self.model.id, func.count('*')
                .label('booked_rooms'))
            .select_from(self.model)
            .where(date_from >= date_from and date_to <= date_to)
            .cte(name='bookings')
        )

        rooms = (
            select(
                self.model.id,
                self.model.quantity,
                func.coalesce(bookings.c.booked_rooms, 0),
                (self.model.quantity - func.coalesce(bookings.c.booked_rooms))
                .label(name='rooms')
                )
            .select_from(self.model)
            .outerjoin(bookings, self.model.id == bookings.c.room_id)
            .cte(name='rooms')
        )
        avaliable_rooms = (
            select(rooms)
            .select_from(rooms)
            .filter(rooms.c.avaliable_rooms > 0)
        )

        print(avaliable_rooms.compile(
            bind=engine, compile_kwargs={'literal_binds': True}))
