from src.models.rooms import RoomsModel
from sqlalchemy import select
from src.schemas.facilities import RoomFacilityAddRequest


async def check_room_existence(room_id, session):
    query = select(RoomsModel).where(RoomsModel.id == room_id)
    room = await session.execute(query)
    result = room.scalars().one_or_none()
    return result


async def room_facilities_manager(
        db,
        room_id: int,
        new_facility_ids: list[int]
):
    current_facility_ids = await db.rooms.get_room_facilities(
        room_id=room_id
    )
    facility_ids_to_delete = [
        id for id in current_facility_ids
        if id not in new_facility_ids
    ]
    facility_ids_to_add = [
        id for id in new_facility_ids
        if id not in current_facility_ids
    ]
    facility_ids_to_add = [
        RoomFacilityAddRequest(room_id=room_id, facility_id=facility_id)
        for facility_id in facility_ids_to_add
    ]
    if facility_ids_to_delete:
        await db.room_facilities.remove_bulk(
            data=facility_ids_to_delete,
            room_id=room_id
        )
    if facility_ids_to_add:
        await db.room_facilities.add_bulk(data=facility_ids_to_add)