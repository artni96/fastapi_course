from datetime import date

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, selectinload

from src.exceptions import DateToLaterThanDateFromException, RoomForHotelNotFoundException
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    RoomDataMapper,
    RoomDataWithFacilitiesMapper,
)
from src.repositories.utils.rooms import (
    extended_room_response,
    extended_rooms_response,
    rooms_ids_for_booking,
)
from src.schemas.rooms import RoomExtendedResponse, RoomPut


class RoomsRepository(BaseRepository):
    model = RoomsModel
    mapper = RoomDataMapper
    exception = RoomForHotelNotFoundException

    async def get_rooms_by_date(self, date_from: date, date_to: date, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        if date_from >= date_to:
            raise  DateToLaterThanDateFromException
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        model_objs = result.unique().scalars().all()
        return [
            RoomDataWithFacilitiesMapper.map_to_domain_entity(model)
            for model in model_objs
        ]

    async def get_one_or_none(self, id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(id=id)
        )
        result = await self.session.execute(query)
        model_obj = result.unique().scalars().one_or_none()
        if model_obj:
            return RoomDataWithFacilitiesMapper.map_to_domain_entity(model_obj)

    async def get_one(self, **filter_by):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            model_obj = result.unique().scalars().one()
        except NoResultFound:
            raise RoomForHotelNotFoundException
        return RoomDataWithFacilitiesMapper.map_to_domain_entity(model_obj)

    async def extended_room_response(
        self, date_from: date, date_to: date, room_id: int, hotel_id: int
    ):
        """Предоставление подробной информации о номере room_id
        в указанный период."""
        queries = extended_room_response(
            date_from=date_from, date_to=date_to, room_id=room_id, hotel_id=hotel_id
        )
        booked_and_avaliable_rooms_info_table = await self.session.execute(
            queries["booked_and_avaliable_rooms_info_table"]
        )
        rooms_facilities = await self.session.execute(queries["room_facilities"])
        try:
            mapped_room_obj = booked_and_avaliable_rooms_info_table.mappings().one_or_none()
            mapped_room_facilities_objs = rooms_facilities.scalar_one()
            if not mapped_room_obj:
                booked_rooms = 0
                avaliable_rooms = mapped_room_facilities_objs.quantity
            else:
                booked_rooms = mapped_room_obj.booked_rooms
                avaliable_rooms = mapped_room_obj.avaliable_rooms
        except NoResultFound:
            raise RoomForHotelNotFoundException
        result = RoomExtendedResponse(
            id=mapped_room_facilities_objs.id,
            hotel_id=mapped_room_facilities_objs.hotel_id,
            title=mapped_room_facilities_objs.title,
            description=mapped_room_facilities_objs.description,
            price=mapped_room_facilities_objs.price,
            quantity=mapped_room_facilities_objs.quantity,
            booked_rooms=booked_rooms,
            avaliable_rooms=avaliable_rooms,
            facilities=mapped_room_facilities_objs.facilities,
        )
        return result

    async def change(self, data: RoomPut, id: int, hotel_id: int, exclude_unset: bool = False):
        query = (
            update(self.model)
            .filter_by(id=id, hotel_id=hotel_id)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        try:
            model_obj = result.scalars().one()
            return self.mapper.map_to_domain_entity(model_obj)
        except NoResultFound as ex:
            raise RoomForHotelNotFoundException
