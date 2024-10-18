from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomInfo
from src.repositories.queries import get_filtered_by_date


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
