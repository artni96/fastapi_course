from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.queries import (get_avaliable_rooms_number,
                                      get_filtered_by_date)
from src.schemas.rooms import RoomInfo, RoomTestResponse
from sqlalchemy import select
from src.db import engine


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomInfo

    async def get_rooms_by_date(self, date_from, date_to, hotel_id):
        avaliable_rooms_id = get_filtered_by_date(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )
        return await self.get_filtered(self.model.id.in_(avaliable_rooms_id))

    async def get_room_with_avaliable_rooms_number(
            self,
            date_from,
            date_to,
            room_id
    ):
        avaliable_rooms_amount = get_avaliable_rooms_number(
            date_from=date_from,
            date_to=date_to,
            room_id=room_id
        )
        print(avaliable_rooms_amount.compile(
            bind=engine, compile_kwargs={'literal_binds': True}))

        result = await self.session.execute(avaliable_rooms_amount)
        model_objs = result.mappings().all()
        return [
            RoomTestResponse.model_validate(room)
            for room in model_objs]
