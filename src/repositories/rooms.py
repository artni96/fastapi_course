from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.queries.rooms import (
    common_response_with_filtered_hotel_room_ids_by_date,
    get_avaliable_rooms_number)
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomExtendedResponse, RoomWithFacilitiesResponse, RoomExtenedeTestResponse
from src.repositories.utils import extended_room_response


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomWithFacilitiesResponse
    mapper = RoomDataMapper

    async def get_rooms_by_date(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        model_objs = result.unique().scalars().all()
        # return [
        #     self.schema.model_validate(model)
        #     for model in model_objs
        # ]
        return [
            self.mapper.map_to_domain_entity(model)
            for model in model_objs
        ]

    async def get_room_with_avaliable_rooms_number(
            self,
            date_from: date,
            date_to: date,
            room_id: int | None = None,
            hotel_id: int | None = None
    ):
        avaliable_rooms_amount = (
            get_avaliable_rooms_number(
                date_from=date_from,
                date_to=date_to,
                room_id=room_id,
                hotel_id=hotel_id
            )
        )

        result = await self.session.execute(avaliable_rooms_amount)
        model_objs = result.mappings().all()
        return [
            RoomExtendedResponse.model_validate(room)
            for room in model_objs]

    async def get_one_or_none(self, hotel_id: int, id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(hotel_id=hotel_id, id=id)
        )
        result = await self.session.execute(query)
        model_obj = result.unique().scalars().one_or_none()
        if model_obj is not None:
            # return self.schema.model_validate(
            #     model_obj, from_attributes=True
            # )
            return self.mapper.map_to_domain_entity(
                model_obj
            )

    async def test_extended_response(
        self,
        date_from: date,
        date_to: date,
        room_id: int
    ):
        pass
        query = extended_room_response(
            date_from=date_from,
            date_to=date_to,
            room_id=room_id
        )
        result = await self.session.execute(query)
        models_obj = result.mappings().all()
        return models_obj
