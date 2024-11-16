from src.config import settings
from src.db import async_session_maker
from src.schemas.hotels import HotelAddPut
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAddPut(title='test hotel', location='test location')
    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel = await db.hotels.add(data=hotel_data, db=db)
        await db.commit()
        print(settings.DB_NAME)
        print(new_hotel)
        assert new_hotel.title == 'test hotel'
