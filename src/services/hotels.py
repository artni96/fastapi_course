from datetime import date

from src.schemas.hotels import HotelResponse, HotelAddRequest, HotelPutRequest, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination,
        date_from: date,
        date_to: date,
        title: str,
        location: str
    ) -> list[HotelResponse] | str | None:
        per_page = pagination.per_page or 3
        result = await self.db.hotels.get_filtered_hotels(
            date_to=date_to,
            date_from=date_from,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
        return result

    async def get_hotel(
        self,
        hotel_id: int
    ):
        return await self.db.hotels.get_one(id=hotel_id)

    async def delete_hotel(self, hotel_id: int):
        result = await self.db.hotels.remove(id=hotel_id)
        await self.db.commit()
        return result

    async def post_hotel(self, hotel_data: HotelAddRequest):
        new_hotel = await self.db.hotels.add(data=hotel_data, db=self.db)
        await self.db.commit()
        return new_hotel

    async def update_hotel(self, hotel_id: int, hotel_data: HotelPutRequest):
        modified_hotel = await self.db.hotels.change(id=hotel_id, data=hotel_data, db=self.db)
        await self.db.commit()
        return modified_hotel

    async def update_hotel_partially(self, hotel_id: int, hotel_data: HotelPatch):
        modified_hotel = await self.db.hotels.change(
            id=hotel_id, exclude_unset=True, data=hotel_data, db=self.db
        )
        await self.db.commit()
        return modified_hotel
