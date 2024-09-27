from sqlalchemy import insert, select, delete, update

from models.hotels import HotelsModel
from src.db import engine
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel

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
        return result.scalars().all()

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
        return result.scalars().one()

    async def remove(self, **filtered_by):
        query = delete(self.model)
        query = await self.filtered_query(
            query=query,
            id=filtered_by['id'],
            title=filtered_by['title'],
            location=filtered_by['location']
        )
        print(query.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        await self.session.execute(query.returning())
        return {'status': 'OK'}

    async def change(self, **data):
        query = update(self.model)
        query = await self.filtered_query(
            query=query,
            id=data['hotel_id'],
            title=data['hotel_title'],
            location=data['hotel_location']
        )
        if data['hotel_data'].location:
            query = query.values(location=data['hotel_data'].location)
        if data['hotel_data'].title:
            query = query.values(title=data['hotel_data'].title)
        print(query.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        await self.session.execute(query.returning())
