from fastapi import APIRouter, Body, Query, Path
from datetime import date, timedelta

from src.api.dependencies import DBDep
from src.schemas.rooms import (RoomCreate, RoomCreateRequest, RoomPatch,
                               RoomPatchRequest, RoomPut, RoomPutRequest)

rooms_router = APIRouter(prefix='/hotels', tags=['Номера'])


@rooms_router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(
    *,
    hotel_id: int = Path(example=1),
    db: DBDep,
    date_from: date = Query(example=date.today()),
    date_to: date = Query(example=date.today() + timedelta(days=3))
):
    rooms = await db.rooms.get_rooms_by_date(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
    return rooms


@rooms_router.post('/{hotel_id}')
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
    await db.commit()
    return room


@rooms_router.get('/{hotel_id}/rooms/{room_id}')
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


@rooms_router.delete('/{hotel_id}/rooms/{room_id}')
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


@rooms_router.put('/{hotel_id}/rooms/{room_id}')
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
    await db.commit()
    return result


@rooms_router.patch('/{hotel_id}/rooms/{room_id}')
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
        **room_data.model_dump(exclude_unset=True)
    )
    result = await db.rooms.change(
        id=room_id,
        hotel_id=hotel_id,
        data=_room_data,
        exclude_unset=True
    )
    await db.commit()
    return result
