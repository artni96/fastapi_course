from src.models.booking import BookingModel
from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.mappers.base import DataMapper
from src.schemas.booking import BookingResponse
from src.schemas.hotels import HotelResponse
from src.schemas.rooms import RoomInfo, RoomWithFacilitiesResponse
from src.schemas.facilities import FacilityResponse
from src.models.facilities import FacilitiesMolel


class HotelDataMapper(DataMapper):
    db_model = HotelsModel
    schema = HotelResponse


class RoomDataMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomWithFacilitiesResponse


class BookingDataMapper(DataMapper):
    db_model = BookingModel
    schema = BookingResponse


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesMolel
    schema = FacilityResponse
