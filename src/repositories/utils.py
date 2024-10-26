from datetime import date
from sqlalchemy import select, func
from src.models.rooms import RoomsModel
from src.models.booking import BookingModel
from sqlalchemy.orm import selectinload, joinedload, load_only
from src.db import engine


def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    booked_rooms_amount_by_date = (
        select(BookingModel.room_id, func.count('*').label('booked_rooms'))
        .select_from(BookingModel)
        .filter(
            BookingModel.date_from <= date_to,
            BookingModel.date_to >= date_from,
        )
        .group_by(BookingModel.room_id)
        .cte(name='booked_rooms_amount_by_date')
    )

    avaliable_rooms_table = (
        select(
            RoomsModel.id.label('room_id'),
            (RoomsModel.quantity - func.coalesce(
                booked_rooms_amount_by_date.c.booked_rooms, 0)).label(
                    'avaliable_rooms'),
        )
        .select_from(RoomsModel)
        .outerjoin(
            booked_rooms_amount_by_date,
            RoomsModel.id == booked_rooms_amount_by_date.c.room_id
        )
        .cte(name='avaliable_rooms_table')
    )

    rooms_ids_for_hotel = (
        select(RoomsModel.id)
        .select_from(RoomsModel)
    )
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel
        .subquery(name='rooms_ids_for_hotel')
    )

    rooms_ids_to_get = (
        select(avaliable_rooms_table.c.room_id)
        .select_from(avaliable_rooms_table)
        .filter(
            avaliable_rooms_table.c.avaliable_rooms > 0,
            avaliable_rooms_table.c.room_id.in_(rooms_ids_for_hotel),
        )
    )
    return rooms_ids_to_get


def extended_room_response(
    date_from: date,
    date_to: date,
    # hotel_id: int | None = None,
    room_id: int | None = None,
):
    booked_rooms_amount_by_date = (
        select(BookingModel.room_id, func.count('*').label('booked_rooms'))
        .select_from(BookingModel)
        .filter(
            BookingModel.date_from <= date_to,
            BookingModel.date_to >= date_from,
            BookingModel.room_id == room_id
        )
        .group_by(BookingModel.room_id)
        .cte(name='booked_rooms_amount_by_date')
    )

    extended_rooms_info_table = (
        select(
            RoomsModel.id.label('room_id'),
            RoomsModel.hotel_id.label('hotel_id'),
            RoomsModel.quantity,
            booked_rooms_amount_by_date.c.booked_rooms.label('booked_rooms'),
            (RoomsModel.quantity - func.coalesce(
                booked_rooms_amount_by_date.c.booked_rooms, 0)).label(
                    'avaliable_rooms'),
        )
        .select_from(booked_rooms_amount_by_date)
        .outerjoin(
            RoomsModel,
            booked_rooms_amount_by_date.c.room_id == RoomsModel.id
        )
    )
    room_facilities = (
        select(RoomsModel)
        .filter(RoomsModel.id == room_id)
        .options(
            load_only(RoomsModel.id)
            .selectinload(RoomsModel.facilities))
    )
    # print(avaliable_rooms_with_facilities_table.compile(
    #     bind=engine, compile_kwargs={'literal_binds': True}))
    # result = [extended_rooms_info_table, room_facilities]
    result = {
        'extended_rooms_info_table': extended_rooms_info_table,
        'room_facilities': room_facilities
    }
    return result
