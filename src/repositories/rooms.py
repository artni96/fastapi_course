from datetime import date
from src.db import engine
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.queries.rooms import (
    common_response_with_filtered_hotel_room_ids_by_date,
    get_avaliable_rooms_number)
from src.schemas.rooms import RoomExtendedResponse
from sqlalchemy import select
from src.schemas.rooms import RoomWithFacilitiesResponse
from sqlalchemy.orm import selectinload, joinedload


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomWithFacilitiesResponse

    async def get_rooms_by_date(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int
    ):
        avaliable_rooms_id = (
            common_response_with_filtered_hotel_room_ids_by_date(
                date_from=date_from,
                date_to=date_to,
                hotel_id=hotel_id
            )
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(avaliable_rooms_id))
        )
        result = await self.session.execute(query)
        model_objs = result.unique().scalars().all()

        return [
            self.schema.model_validate(model)
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
        # print(avaliable_rooms_amount.compile(
        #     bind=engine, compile_kwargs={'literal_binds': True}))

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
            return self.schema.model_validate(
                model_obj, from_attributes=True
            )
