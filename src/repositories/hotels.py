from datetime import date

from sqlalchemy import insert, select

from src.db import engine
from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.queries.rooms import (
    common_response_with_filtered_hotel_room_ids_by_date, get_filtered_by_date)
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    def filtered_query(self, query, location=None, title=None, id=None):
        if id is not None:
            query = query.filter_by(id=id)
        if title is not None:
            query = query.filter(self.model.title.icontains(title))
        if location is not None:
            query = query.filter(self.model.location.icontains(
                location))
        return query

    async def get_filtered_hotels(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            offset: int,
            limit: int
    ):
        avaliable_room_ids = (
            common_response_with_filtered_hotel_room_ids_by_date(
                date_from=date_from,
                date_to=date_to,
                hotel_id=id
            )
        )
        filter_room_ids = self.filtered_query(
            query=avaliable_room_ids,
            location=location,
            title=title
        )
        hotels_with_avaliable_rooms = (
            select(RoomsModel.hotel_id)
            .filter(RoomsModel.id.in_(filter_room_ids))
        )
        paginated_hotels_with_avaliable_rooms = (
            hotels_with_avaliable_rooms.limit(limit).offset(offset)
        )
        print(paginated_hotels_with_avaliable_rooms.compile(
            bind=engine, compile_kwargs={'literal_binds': True}))
        return await self.get_filtered(
            HotelsModel.id.in_(paginated_hotels_with_avaliable_rooms))

    async def add(self, hotel: HotelsModel):
        new_hotel_stmt = (
            insert(self.model).values(**hotel.model_dump()).returning(
                self.model)
        )
        print(new_hotel_stmt.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        result = await self.session.execute(new_hotel_stmt)
        model_obj = result.scalars().one()
        return Hotel.model_validate(
            model_obj, from_attributes=True
        )
