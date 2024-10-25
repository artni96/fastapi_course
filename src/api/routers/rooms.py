from datetime import date, datetime

from fastapi import APIRouter, Body, Path, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAddRequest
from src.schemas.rooms import (RoomCreate, RoomCreateRequest, RoomPatch,
                               RoomPatchRequest, RoomPut, RoomPutRequest)


rooms_router = APIRouter(prefix='/hotels', tags=['Номера'])


@rooms_router.get(
    '/{hotel_id}/rooms',
    summary=(
        'Получение информации о свободных номерах (без точного количества)'
        ' отеля по "hotel_id" в указанный период'
    )
)
async def get_hotel_rooms(
    *,
    hotel_id: int = Path(example=1),
    db: DBDep,
    date_from: date | str = Query(example='18.10.2024'),
    date_to: date | str = Query(example='21.10.2024'),
) -> list:
    try:
        date_to = datetime.strptime(date_to, '%d.%m.%Y').date()
        date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
    except ValueError:
        return 'Укажите даты в формате dd.mm.yyyy'
    rooms = await db.rooms.get_rooms_by_date(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
    return rooms


@rooms_router.post(
    '/{hotel_id}',
    summary='Создание нового типа номеров для отеля "hotel_id"')
async def create_room(
    *,
    hotel_id: int,
    room_data: RoomCreateRequest = Body(
        openapi_examples=RoomCreateRequest.Config.schema_extra['examples']
    ),
    db: DBDep
):
    _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(data=_room_data)
    facilities = [
        RoomFacilityAddRequest(room_id=room.id, facility_id=facility_id)
        for facility_id in room_data.facility_ids
    ]
    await db.room_facilities.add_bulk(data=facilities)

    await db.commit()
    return room


@rooms_router.get(
    '/{hotel_id}/rooms/{room_id}',
    summary=(
        'Получение общей информации о всех типах номеров для '
        'отеля "hotel_id"'
    )
)
async def get_hotel_room(
    hotel_id: int,
    room_id: int,
    db: DBDep
):
    room = await db.rooms.get_one_or_none(
        hotel_id=hotel_id,
        id=room_id
    )
    return room


@rooms_router.get(
    '/{hotel_id}/extended-rooms/',
    summary=(
        'Получение подробной информации о количестве свободных номеров'
        ' отеля по "hotel_id" в указанный период'
    )
)
async def get_filtered_hotel_room_by_date(
    *,
    hotel_id: int,
    date_from: date | str = Query(example='18.10.2024'),
    date_to: date | str = Query(example='21.10.2024'),
    db: DBDep
):
    try:
        date_to = datetime.strptime(date_to, '%d.%m.%Y').date()
        date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
    except ValueError:
        return 'Укажите даты в формате dd.mm.yyyy'

    room = await db.rooms.get_room_with_avaliable_rooms_number(
        # room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        hotel_id=hotel_id
    )
    return room


@rooms_router.get(
    '/{hotel_id}/extended-rooms/{room_id}',
    summary=(
        'Получение подробной информации о количестве свободных номеров'
        ' определенного типа "room_id" в указанный период'
    )
)
async def get_rooms_by_date(
    *,
    hotel_id: int,
    room_id: int,
    date_from: date | str = Query(example='18.10.2024'),
    date_to: date | str = Query(example='21.10.2024'),
    db: DBDep
):
    try:
        date_to = datetime.strptime(date_to, '%d.%m.%Y').date()
        date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
    except ValueError:
        return 'Укажите даты в формате dd.mm.yyyy'

    room = await db.rooms.get_room_with_avaliable_rooms_number(
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        hotel_id=hotel_id
    )
    return room


@rooms_router.delete(
    '/{hotel_id}/rooms/{room_id}',
    summary=(
        'Удаление типа номер по "room_id" для отеля "hotel_id"'
    )
)
async def remove_hotel_room(
    hotel_id: int,
    room_id: int,
    db: DBDep
):
    result = await db.rooms.remove(
        hotel_id=hotel_id,
        id=room_id
    )
    await db.commit()
    return result


@rooms_router.put(
    '/{hotel_id}/rooms/{room_id}',
    summary=(
        'Полное обновление инофрмации о типе номеров по "room_id" для отеля '
        '"hotel_id"'
    )
)
async def update_hotel_room(
    *,
    hotel_id: int,
    room_id: int,
    room_data: RoomPutRequest = Body(
        openapi_examples=RoomPutRequest.Config.schema_extra['examples']
    ),
    db: DBDep
):

    _room_data = RoomPut(hotel_id=hotel_id, **room_data.model_dump())
    result = await db.rooms.change(
        id=room_id,
        hotel_id=hotel_id,
        data=_room_data,
        exclude_unset=False
    )
    new_facility_ids = room_data.facility_ids
    await db.room_facilities.room_facility_manager(
        room_id=room_id,
        new_facility_ids=new_facility_ids
    )
    await db.commit()
    return result


@rooms_router.patch(
    '/{hotel_id}/rooms/{room_id}',
    summary=(
        'Частичное обновление инофрмации о типе номеров по "room_id" для '
        '"отеля hotel_id"'
    )
)
async def update_hotel_room_partially(
    *,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(
        openapi_examples=RoomPatchRequest.Config.schema_extra['examples']
    ),
    db: DBDep
):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(
            exclude_unset=True, exclude='facility_ids')
    )
    result = await db.rooms.change(
        id=room_id,
        hotel_id=hotel_id,
        data=_room_data,
        exclude_unset=True
    )
    new_facility_ids = room_data.facility_ids
    if new_facility_ids:
        if new_facility_ids:
            await db.room_facilities.room_facility_manager(
                room_id=room_id,
                new_facility_ids=new_facility_ids
            )
        await db.commit()
    return result


@rooms_router.get('/{hotel_id}/roomsextended-test/{room_id}')
async def get_avaliable_rooms(
    *,
    date_from: date | str = Query(example='18.10.2024'),
    date_to: date | str = Query(example='21.10.2024'),
    room_id: int,
    db: DBDep
):
    try:
        date_to = datetime.strptime(date_to, '%d.%m.%Y').date()
        date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
    except ValueError:
        return 'Укажите даты в формате dd.mm.yyyy'
    return await db.rooms.test_extended_response(
        date_from=date_from,
        date_to=date_to,
        room_id=room_id
    )
