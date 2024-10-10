from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomInfo


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomInfo
