from src.db import async_session_maker_null_pool
from src.schemas.hotels import HotelAddPut
from src.utils.db_manager import DBManager
from src.base import *


async def test_add_hotel():
    hotel_data = HotelAddPut(title="Hotel 5 stars", location="Сочи")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_data, db=db)
        await  db.commit()
        assert new_hotel_data.title == 'Hotel 5 stars'
        assert new_hotel_data.location == 'Сочи'
