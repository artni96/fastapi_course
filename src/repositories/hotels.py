from datetime import date

from sqlalchemy import insert, select

from src.db import engine
from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper = HotelDataMapper

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
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to
        )
        hotels_ids_to_get = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )
        query = select(self.model).filter(self.model.id.in_(hotels_ids_to_get))
        filtered_query_by_params = self.filtered_query(
            query=query,
            location=location,
            title=title
        )
        filtered_query_by_params = filtered_query_by_params.limit(
            limit).offset(offset)
        result = await self.session.execute(filtered_query_by_params)
        return [self.mapper.map_to_domain_entity(hotel)
                for hotel in result.scalars().all()]

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
        return self.mapper.map_to_domain_entity(model_obj)
