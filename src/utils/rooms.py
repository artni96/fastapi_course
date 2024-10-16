from src.models.rooms import RoomsModel
from sqlalchemy import select


async def check_room_existence(room_id, session):
    query = select(RoomsModel).where(RoomsModel.id == room_id)
    room = await session.execute(query)
    result = room.scalars().one_or_none()
    return result
