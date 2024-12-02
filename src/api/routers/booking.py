from fastapi import APIRouter, Body, status, HTTPException

from src.api.dependencies import DBDep, PaginationDep, UserDep
from src.api.exceptions import NoAvailableRoomsException, RoomNotFoundException, BookingNotFoundException, \
    DateToLaterThanDateFromException, DateToLaterThanCurrentTimeException
from src.schemas.booking import (
    BookingCreate,
    BookingCreateRequest,
    BookingUpdateRequest,
)


booking_router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@booking_router.get("", summary="Получение информации всех бронированиях")
async def get_all_bookings(db: DBDep, user: UserDep, pagination: PaginationDep):
    per_page = pagination.per_page or 3
    bookings = await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )
    return bookings


@booking_router.get(
    "/me",
    summary=(
        "Получение информации о всех бронированиях номеров авторизованного "
        "пользователя"
    ),
)
async def get_my_bookings(db: DBDep, user: UserDep, pagination: PaginationDep):
    per_page = pagination.per_page or 3
    bookings = await db.bookings.get_all(
        limit=per_page, offset=per_page * (pagination.page - 1), user_id=user.id
    )
    return bookings


@booking_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового бронирования номера",
)
async def create_booking(
    *,
    booking_data: BookingCreateRequest = Body(
        openapi_examples=BookingCreateRequest.model_config["json_schema_extra"]
    ),
    db: DBDep,
    user: UserDep,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        return {"status": "Номер с указанным id не найден"}
    price = room.price
    _booking_data = BookingCreate(
        price=price, user_id=user.id, **booking_data.model_dump()
    )
    try:
        result = await db.bookings.add(data=_booking_data)
    except NoAvailableRoomsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет свободных номеров",
        )
    await db.commit()
    return result


@booking_router.patch(
    "/{booking_id}", summary='Частичное обновление бронирования номера по "booking_id"'
)
async def update_booking(
    booking_id: int,
    db: DBDep,
    user: UserDep,
    booking_data: BookingUpdateRequest,
):
    # booking = await db.bookings.get_one_or_none(id=booking_id)
    # if not booking:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Бронирование с указанным id не найдено!"
    #     )
    # if booking_data.room_id:
    #     room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    # else:
    #     room = await db.rooms.get_one_or_none(id=booking.room_id)
    # price = room.price
    # _booking_data = BookingUpdate(
    #     # price=price,
    #     **booking_data.model_dump()
    # )

    # if booking.user_id == user.id:
    try:
        result = await db.bookings.change(
            booking_data=booking_data,
            exclude_unset=True,
            booking_id=booking_id,
            db=db,
            user_id=user.id
        )
    except RoomNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
    except BookingNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
    except DateToLaterThanDateFromException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    except DateToLaterThanCurrentTimeException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    await db.commit()
    return result

    return "Только автор может измениять данные!"
