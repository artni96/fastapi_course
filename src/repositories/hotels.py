from sqlalchemy import insert, select, delete

from models.hotels import HotelsModel
from src.db import engine
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            title,
            location,
            offset,
            limit
    ):
        query = select(self.model)
        if title:
            query = query.filter(self.model.title.icontains(title))
        if location:
            query = query.filter(self.model.location.icontains(location))
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
        if filtered_by['id'] is not None:
            query = query.filter_by(id=filtered_by['id'])
        if filtered_by['location'] is not None:
            query = query.filter(self.model.location.icontains(
                filtered_by['location']))
        if filtered_by['title'] is not None:
            query = query.filter(self.model.title.icontains(
                filtered_by['title']))
        print(query.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        result = await self.session.execute(query)
        if len(result.scalars().all()):
            return {'status': 'OK'}
        return {'status': 'Not found'}
