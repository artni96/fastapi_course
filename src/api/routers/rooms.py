from datetime import date, timedelta

from fastapi import APIRouter, Body, Path, Query, status, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import NotFoundException, DateToLaterThanDateFromException, \
    HotelNotFoundException, RoomForHotelNotFoundException
from src.schemas.rooms import (
    RoomCreateRequest,
    RoomPatch,
    RoomPatchRequest,
    RoomPutRequest,
)
from src.services.rooms import RoomService


rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get(
    "/{hotel_id}/rooms",
    summary=(
        "Получение информации о свободных номерах (без точного количества)"
        ' отеля по "hotel_id" в указанный период'
    ),
)
async def get_hotel_rooms(
    *,
    hotel_id: int = Path(
        examples=[
            1,
        ]
    ),
    db: DBDep,
    date_from: date = Query(
        default=date.today() + timedelta(days=1)
    ),
    date_to: date = Query(
        default=date.today() + timedelta(days=2)
    ),
) -> list:
    try:
        rooms = await RoomService(db).get_hotel_rooms(hotel_id, date_from, date_to)
    except DateToLaterThanDateFromException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет свободных номеров')
    return rooms


@rooms_router.post(
    "/{hotel_id}",
    summary='Создание нового типа номеров для отеля "hotel_id"',
    status_code=status.HTTP_201_CREATED,
)
async def create_room(
    *,
    hotel_id: int,
    room_data: RoomCreateRequest = Body(
        openapi_examples=RoomCreateRequest.model_config["json_schema_extra"]
    ),
    db: DBDep,
):
    try:
        return await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)


@rooms_router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary=("Получение общей информации о всех типах номеров для " 'отеля "hotel_id"'),
)
async def get_hotel_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        room = await RoomService(db).get_hotel_room(hotel_id, room_id)
    except RoomForHotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail(hotel_id, room_id))
    return room


@rooms_router.get(
    "/{hotel_id}/extended-rooms/{room_id}",
    summary=(
        "Получение подробной информации о количестве свободных номеров"
        ' определенного типа "room_id" в указанный период'
    ),
)
async def get_rooms_by_date(
    *,
    date_from: date = Query(examples=[date.today() + timedelta(days=1)]),
    date_to: date = Query(examples=[date.today() + timedelta(days=2)]),
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        return await RoomService(db).get_rooms_with_ext_info_by_date(
            date_from=date_from, date_to=date_to, room_id=room_id, hotel_id=hotel_id
        )
    except RoomForHotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail(hotel_id, room_id))


@rooms_router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary='Удаление типа номер по "room_id" для отеля "hotel_id"',
)
async def remove_hotel_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        result = await RoomService(db).remove_hotel_room(hotel_id, room_id)
    except RoomForHotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail(hotel_id, room_id))
    return result


@rooms_router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary=(
        'Полное обновление инофрмации о типе номеров по "room_id" для отеля '
        '"hotel_id"'
    ),
)
async def update_hotel_room(
    *,
    hotel_id: int,
    room_id: int,
    room_data: RoomPutRequest = Body(
        openapi_examples=RoomPutRequest.model_config["json_schema_extra"]
    ),
    db: DBDep,
):
    try:
        return await RoomService(db).update_hotel_room(hotel_id, room_id, room_data)
    except RoomForHotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail(hotel_id, room_id))

@rooms_router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary=(
        'Частичное обновление инофрмации о типе номеров по "room_id" для '
        '"отеля hotel_id"'
    ),
)
async def update_hotel_room_partially(
    *,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(
        openapi_examples=RoomPatchRequest.model_config["json_schema_extra"]
    ),
    db: DBDep,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True, exclude="facility_ids"),
    )
    try:
        return await RoomService(db).update_hotel_room_partially(hotel_id, room_id, room_data)
    except RoomForHotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail(hotel_id, room_id))
