from fastapi import APIRouter, Body

from src.api.dependencies import SessionDep
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomBase, RoomPatch


rooms_router = APIRouter(prefix='/hotels', tags=['Номера'])


@rooms_router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(
    hotel_id: int,
    session: SessionDep
):
    rooms = await RoomsRepository(session).get_all(hotel_id)
    return rooms


@rooms_router.post('/{hotel_id}')
async def create_room(
    *,
    hotel_id: int,
    room_data: RoomBase = Body(
        openapi_examples=RoomBase.Config.schema_extra['examples']
    ),
    session: SessionDep
):
    room = await RoomsRepository(session).add(
        room_data=room_data, hotel_id=hotel_id
    )
    await session.commit()
    return room


@rooms_router.get('/{hotel_id}/rooms/{room_id}')
async def get_hotel_room(
    hotel_id: int,
    room_id: int,
    session: SessionDep
):
    room = await RoomsRepository(session).get_one_or_none(
        hotel_id=hotel_id,
        room_id=room_id
    )
    return room


@rooms_router.delete('/{hotel_id}/rooms/{room_id}')
async def remove_hotel_room(
    hotel_id: int,
    room_id: int,
    session: SessionDep
):
    result = await RoomsRepository(session).remove(
        hotel_id=hotel_id,
        room_id=room_id
    )
    await session.commit()
    return result


@rooms_router.put('/{hotel_id}/rooms/{room_id}')
async def update_hotel_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomBase,
    session: SessionDep
):
    result = await RoomsRepository(session).change(
        hotel_id=hotel_id,
        room_id=room_id,
        room_data=room_data,
        exclude_unset=False
    )
    await session.commit()
    return result


@rooms_router.patch('/{hotel_id}/rooms/{room_id}')
async def update_hotel_room_partially(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatch,
    session: SessionDep
):
    result = await RoomsRepository(session).change(
        hotel_id=hotel_id,
        room_id=room_id,
        room_data=room_data,
        exclude_unset=True
    )
    await session.commit()
    return result
