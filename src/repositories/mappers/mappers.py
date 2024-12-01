from src.models import User
from src.models.booking import BookingModel
from src.models.facilities import FacilitiesMolel
from src.models.hotels import HotelsModel
from src.models.images import ImagesModel
from src.models.rooms import RoomsModel
from src.repositories.mappers.base import DataMapper
from src.schemas.booking import BookingResponse
from src.schemas.facilities import FacilityResponse
from src.schemas.hotels import HotelResponse
from src.schemas.images import ImageRead
from src.schemas.rooms import RoomInfo, RoomWithFacilitiesResponse
from src.schemas.users import User as UserRead


class HotelDataMapper(DataMapper):
    db_model = HotelsModel
    schema = HotelResponse


class RoomDataMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomInfo


class RoomDataWithFacilitiesMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomWithFacilitiesResponse


class BookingDataMapper(DataMapper):
    db_model = BookingModel
    schema = BookingResponse


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesMolel
    schema = FacilityResponse


class ImageMapper(DataMapper):
    db_model = ImagesModel
    schema = ImageRead


class UserMapper(DataMapper):
    db = User
    schema = UserRead
