from fastapi import APIRouter, Body, status, HTTPException

from src.api.dependencies import DBDep, PaginationDep, UserDep
from src.exceptions import NoAvailableRoomsException, RoomForHotelNotFoundException, BookingNotFoundException, \
    DateToLaterThanDateFromException, DateToLaterThanCurrentTimeException, RoomNotFoundException, OnlyForAuthorException
from src.schemas.booking import (
    BookingCreateRequest,
    BookingUpdateRequest,
)
from src.services.bookings import BookingService

booking_router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@booking_router.get("", summary="Получение информации всех бронированиях")
async def get_all_bookings(db: DBDep, user_id: UserDep, pagination: PaginationDep):
    bookings = await BookingService(db).get_all_bookings(pagination)
    return bookings


@booking_router.get(
    "/me",
    summary=(
        "Получение информации о всех бронированиях номеров авторизованного "
        "пользователя"
    ),
)
async def get_my_bookings(db: DBDep, user: UserDep, pagination: PaginationDep):
    try:
        bookings = await BookingService(db).get_my_bookings(user, pagination)
        return bookings
    except Exception:
        raise HTTPException(status_code=500)


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
    user_id: UserDep,
):
    try:
        # result = await db.bookings.add(booking_data=booking_data, user_id=user, db=db)
        result = await BookingService(db).create_booking(booking_data, user_id)
    except RoomNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail(booking_data.room_id)
        )
    except NoAvailableRoomsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет свободных номеров",
        )
    except DateToLaterThanDateFromException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    await db.commit()
    return result


@booking_router.patch(
    "/{booking_id}", summary='Частичное обновление бронирования номера по "booking_id"'
)
async def update_booking(
    booking_id: int,
    db: DBDep,
    user_id: UserDep,
    booking_data: BookingUpdateRequest,
):
    try:
        result = await BookingService(db).update_booking(booking_id, user_id, booking_data)
    except RoomForHotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер не найден')
    except BookingNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
    except DateToLaterThanDateFromException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    except DateToLaterThanCurrentTimeException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    except OnlyForAuthorException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    await db.commit()
    return result

@booking_router.delete(
    "/{booking_id}", summary='Удаление бронирования по booking_id'
)
async def remove_booking(
    booking_id: int,
    db: DBDep,
    user: UserDep,
):
    try:
        return await BookingService(db).remove_booking(booking_id=booking_id, user=user)
    except BookingNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
    except OnlyForAuthorException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
