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
        mapped_room_obj = booked_and_avaliable_rooms_info_table.mappings().one_or_none()
        mapped_room_facilities_objs = rooms_facilities.scalars().one_or_none()
        if not mapped_room_obj:
            booked_rooms = 0
            avaliable_rooms = mapped_room_facilities_objs.quantity
        else:
            booked_rooms = mapped_room_obj.booked_rooms
            avaliable_rooms = mapped_room_obj.avaliable_rooms
        if not mapped_room_facilities_objs:
            return {"status": "Room with given room_id in the hotel has not found"}
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


    async def extended_rooms_response_manager(
        self, date_from: date, date_to: date, hotel_id: int
    ):
        """Предоставление списка с подробной информацией о номерах отеля
        hotel_id в указанный период."""
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
        queries = extended_rooms_response(
            date_from=date_from, date_to=date_to, rooms_id=rooms_ids_to_get
        )
        booked_and_avaliable_rooms_info_table = await self.session.execute(
            queries["booked_and_avaliable_rooms_info_table"]
        )
        rooms_facilities = await self.session.execute(
            queries["rooms_info_with_facilities"]
        )
        mapped_rooms_objs = booked_and_avaliable_rooms_info_table.mappings().all()
        mapped_room_facilities_objs = rooms_facilities.scalars().all()
        result = list()
        for obj in mapped_room_facilities_objs:
            for i in range(len(mapped_rooms_objs)):
                current_obj = RoomExtendedResponse(
                    id=obj.id,
                    hotel_id=obj.hotel_id,
                    title=obj.title,
                    description=obj.description,
                    price=obj.price,
                    quantity=obj.quantity,
                    facilities=obj.facilities,
                )
                if (
                    len(mapped_rooms_objs) > 0
                    and obj.id == mapped_rooms_objs[i].room_id
                ):
                    current_obj.booked_rooms = mapped_rooms_objs[i].booked_rooms
                    current_obj.avaliable_rooms = mapped_rooms_objs[i].avaliable_rooms
                    result.append(current_obj)
                    mapped_rooms_objs.pop(i)
                else:
                    current_obj.booked_rooms = 0
                    current_obj.avaliable_rooms = obj.quantity
                    result.append(current_obj)
        return result
