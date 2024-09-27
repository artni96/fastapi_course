from sqlalchemy import insert, select

from models.hotels import HotelsModel
from schemas.hotels import Hotel
from src.db import engine
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def filtered_query(self, query, location=None, title=None, id=None):
        if id is not None:
            query = query.filter_by(id=id)
        if title is not None:
            query = query.filter(self.model.title.icontains(title))
        if location is not None:
            query = query.filter(self.model.location.icontains(
                location))
        return query

    async def get_all(
            self,
            title,
            location,
            offset,
            limit
    ):
        query = select(self.model)
        query = await self.filtered_query(
            query=query,
            title=title,
            location=location
        )
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [
            Hotel.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]

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
