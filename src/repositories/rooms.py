from src.models.rooms import RoomsModel
from src.models.booking import BookingModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomInfo
from sqlalchemy import select, func


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomInfo

    async def get_filtered_by_date(self, date_from, date_to, hotel_id):
        bookings_by_date = (
            select(
                BookingModel.room_id,
                func.count('*').label('booked_rooms'))
            .select_from(BookingModel)
            .where(
                BookingModel.date_from >= date_from,
                BookingModel.date_to <= date_to)
            .group_by(BookingModel.room_id)
            .cte(name='bookings')
        )

        booked_rooms = (
            select(
                self.model.id,
                self.model.quantity,
                func.coalesce(bookings_by_date.c.booked_rooms, 0),
                (self.model.quantity - func.coalesce(
                    bookings_by_date.c.booked_rooms))
                .label(name='rooms')
                )
            .select_from(self.model)
            .outerjoin(
                bookings_by_date, self.model.id == bookings_by_date.c.room_id
            )
            .cte(name='rooms')
        )

        hotel_room_id_list = (
            select(self.model.id)
            .select_from(self.model)
            .where(self.model.hotel_id == hotel_id)
            .subquery(name='hotel_room_id_list')
            # subquery чисто для понимания, что это подзапрос
        )

        avaliable_rooms_id = (
            select(booked_rooms.c.id)
            .select_from(booked_rooms)
            .where(booked_rooms.c.id.in_(hotel_room_id_list))
            .filter(booked_rooms.c.rooms > 0)
        )

        # print(avaliable_rooms_id.compile(
        #     bind=engine, compile_kwargs={'literal_binds': True}))
        # return await self.get_filtered(self.model.id.in_(avaliable_rooms_id))
        return await self.get_filtered(self.model.id.in_(avaliable_rooms_id))
