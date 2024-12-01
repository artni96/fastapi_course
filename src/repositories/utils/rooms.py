from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import load_only

from src.models.booking import BookingModel
from src.models.rooms import RoomsModel


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    booked_rooms_amount_by_date = (
        select(BookingModel.room_id, func.count("*").label("booked_rooms"))
        .select_from(BookingModel)
        .filter(
            BookingModel.date_from <= date_to,
            BookingModel.date_to >= date_from,
        )
        .group_by(BookingModel.room_id)
        .cte(name="booked_rooms_amount_by_date")
    )

    avaliable_rooms_table = (
        select(
            RoomsModel.id.label("room_id"),
            (
                RoomsModel.quantity
                - func.coalesce(booked_rooms_amount_by_date.c.booked_rooms, 0)
            ).label("avaliable_rooms"),
        )
        .select_from(RoomsModel)
        .outerjoin(
            booked_rooms_amount_by_date,
            RoomsModel.id == booked_rooms_amount_by_date.c.room_id,
        )
        .cte(name="avaliable_rooms_table")
    )

    rooms_ids_for_hotel = select(RoomsModel.id).select_from(RoomsModel)
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.scalar_subquery()

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
    hotel_id: int | None = None,
    room_id: int | None = None,
):
    booked_rooms_amount_by_date = (
        select(
            BookingModel.room_id,
            func.coalesce(func.count("*"), 0).label("booked_rooms"),
        )
        .select_from(BookingModel)
        .filter(
            BookingModel.date_from <= date_to,
            BookingModel.date_to >= date_from,
            BookingModel.room_id == room_id,
        )
        .group_by(BookingModel.room_id)
        .cte(name="booked_rooms_amount_by_date")
    )

    booked_and_avaliable_rooms_info_table = (
        select(
            booked_rooms_amount_by_date.c.booked_rooms.label("booked_rooms"),
            (
                RoomsModel.quantity
                - func.coalesce(booked_rooms_amount_by_date.c.booked_rooms, 0)
            ).label("avaliable_rooms"),
        )
        .select_from(booked_rooms_amount_by_date)
        .outerjoin(RoomsModel, booked_rooms_amount_by_date.c.room_id == RoomsModel.id)
    )
    room_facilities = (
        select(RoomsModel)
        .filter(RoomsModel.id == room_id, RoomsModel.hotel_id == hotel_id)
        .select_from(RoomsModel)
        .options(
            load_only(
                RoomsModel.id,
                RoomsModel.hotel_id,
                RoomsModel.title,
                RoomsModel.description,
                RoomsModel.price,
                RoomsModel.quantity,
            ).selectinload(RoomsModel.facilities)
        )
    )
    result = {
        "booked_and_avaliable_rooms_info_table": (
            booked_and_avaliable_rooms_info_table
        ),
        "room_facilities": room_facilities,
    }
    return result


def extended_rooms_response(
    date_from: date,
    date_to: date,
    rooms_id: list[int] | None = None,
):
    booked_rooms_amount_by_date = (
        select(
            BookingModel.room_id,
            func.coalesce(func.count("*"), 0).label("booked_rooms"),
        )
        .select_from(BookingModel)
        .filter(
            BookingModel.date_from <= date_to,
            BookingModel.date_to >= date_from,
            BookingModel.room_id.in_(rooms_id),
        )
        .group_by(BookingModel.room_id)
        .cte(name="booked_rooms_amount_by_date_1")
    )

    booked_and_avaliable_rooms_info_table = (
        select(
            booked_rooms_amount_by_date.c.room_id.label("room_id"),
            booked_rooms_amount_by_date.c.booked_rooms.label("booked_rooms"),
            (
                RoomsModel.quantity
                - func.coalesce(booked_rooms_amount_by_date.c.booked_rooms, 0)
            ).label("avaliable_rooms"),
        )
        .select_from(booked_rooms_amount_by_date)
        .outerjoin(RoomsModel, booked_rooms_amount_by_date.c.room_id == RoomsModel.id)
    )
    rooms_info_with_facilities = (
        select(RoomsModel)
        .filter(
            RoomsModel.id.in_(rooms_id),
        )
        .select_from(RoomsModel)
        .options(
            load_only(
                RoomsModel.id,
                RoomsModel.hotel_id,
                RoomsModel.title,
                RoomsModel.description,
                RoomsModel.price,
                RoomsModel.quantity,
            ).selectinload(RoomsModel.facilities)
        )
    )
    result = {
        "booked_and_avaliable_rooms_info_table": (
            booked_and_avaliable_rooms_info_table
        ),
        "rooms_info_with_facilities": rooms_info_with_facilities,
    }
    return result


async def check_room_existence(room_id, session):
    query = select(RoomsModel).where(RoomsModel.id == room_id)
    room = await session.execute(query)
    result = room.scalars().one_or_none()
    return result
