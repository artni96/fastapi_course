from datetime import date
from src.db import engine
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.queries.rooms import (
    common_response_with_filtered_hotel_room_ids_by_date,
    get_avaliable_rooms_number)
from src.schemas.rooms import RoomInfo, RoomTestResponse
from sqlalchemy import select
from src.models.facilities import RoomFacilitiesModel


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomInfo

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
        return await self.get_filtered(self.model.id.in_(avaliable_rooms_id))

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
        print(avaliable_rooms_amount.compile(
            bind=engine, compile_kwargs={'literal_binds': True}))

        result = await self.session.execute(avaliable_rooms_amount)
        model_objs = result.mappings().all()
        return [
            RoomTestResponse.model_validate(room)
            for room in model_objs]

    async def get_room_facilities(
        self, room_id: int
    ):
        room_facility_ids = select(RoomFacilitiesModel.facility_id).where(
            RoomFacilitiesModel.room_id == room_id)
        result = await self.session.execute(room_facility_ids)
        return result.scalars().all()
