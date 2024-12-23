from src.schemas.hotels import HotelAddPut
from src.base import *  # noqa F401


async def test_add_hotel(db):
    hotel_data = HotelAddPut(title="Hotel 5 stars", location="Сочи")
    new_hotel_data = await db.hotels.add(hotel_data, db=db)
    await db.commit()
    assert new_hotel_data.title == "Hotel 5 stars"
    assert new_hotel_data.location == "Сочи"
