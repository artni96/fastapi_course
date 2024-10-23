from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.models.booking import BookingModel
from src.models.rooms import RoomsModel


def get_filtered_by_date(
    date_from: date,
    date_to: date,
):
    bookings_by_date = (
        select(
            BookingModel.room_id,
            func.count('*').label('booked_rooms'))
        .select_from(BookingModel)
        .where(
            BookingModel.date_from <= date_to,
            BookingModel.date_to >= date_from)
        .group_by(BookingModel.room_id)
        .cte(name='bookings')
    )

    room_info = (
        select(
            RoomsModel.hotel_id.label('hotel_id'),
            RoomsModel.id,
            RoomsModel.quantity.label('quantity'),
            RoomsModel.title.label('title'),
            RoomsModel.description.label('description'),
            RoomsModel.price.label('price'),
            func.coalesce(
                bookings_by_date.c.booked_rooms, 0).label('booked_rooms'),
            (RoomsModel.quantity - func.coalesce(
                bookings_by_date.c.booked_rooms))
            .label(name='avaliable_rooms')
            )
        .select_from(bookings_by_date)
        .outerjoin(
            RoomsModel, RoomsModel.id == bookings_by_date.c.room_id
        )
    )
    return room_info


def common_response_with_filtered_hotel_room_ids_by_date(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    booked_rooms = get_filtered_by_date(date_from=date_from, date_to=date_to)
    avaliable_room_ids = (
        select(booked_rooms.c.id)
        .select_from(booked_rooms)
        .filter(booked_rooms.c.avaliable_rooms > 0)
    )

    hotel_room_ids_list = (
        select(RoomsModel.id)
        .select_from(RoomsModel)
        .where(RoomsModel.hotel_id == hotel_id)
        .subquery(name='hotel_room_id_list')
        # subquery чисто для понимания, что это подзапрос
    )

    if hotel_id is not None:
        avaliable_room_ids = avaliable_room_ids.where(booked_rooms.c.id.in_(hotel_room_ids_list))

    # print(avaliable_rooms_id.compile(
    #     bind=engine, compile_kwargs={'literal_binds': True}))
    return avaliable_room_ids


def get_avaliable_rooms_number(
    date_from: date,
    date_to: date,
    room_id: int | None = None,
    hotel_id: int | None = None
):
    booked_rooms = get_filtered_by_date(
        date_from=date_from,
        date_to=date_to
    )
    if room_id is not None:
        result = booked_rooms.where(
            RoomsModel.id == room_id)
    if hotel_id is not None:
        result = booked_rooms.where(
            RoomsModel.hotel_id == hotel_id)
    return result
