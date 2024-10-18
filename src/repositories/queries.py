from src.models.rooms import RoomsModel
from src.models.booking import BookingModel
from datetime import date

from sqlalchemy import select, func


def get_filtered_by_date(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None
):
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
            RoomsModel.id,
            RoomsModel.quantity,
            func.coalesce(bookings_by_date.c.booked_rooms, 0),
            (RoomsModel.quantity - func.coalesce(
                bookings_by_date.c.booked_rooms))
            .label(name='rooms')
            )
        .select_from(RoomsModel)
        .outerjoin(
            bookings_by_date, RoomsModel.id == bookings_by_date.c.room_id
        )
        .cte(name='booked_rooms')
    )

    hotel_room_id_list = (
        select(RoomsModel.id)
        .select_from(RoomsModel)
        .where(RoomsModel.hotel_id == hotel_id)
        .subquery(name='hotel_room_id_list')
        # subquery чисто для понимания, что это подзапрос
    )

    avaliable_rooms_id = (
        select(booked_rooms.c.id)
        .select_from(booked_rooms)
        .filter(booked_rooms.c.rooms > 0)
    )
    if hotel_id is not None:
        avaliable_rooms_id.where(booked_rooms.c.id.in_(hotel_room_id_list))

    # print(avaliable_rooms_id.compile(
    #     bind=engine, compile_kwargs={'literal_binds': True}))
    return avaliable_rooms_id
