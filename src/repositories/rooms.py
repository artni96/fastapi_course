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
from src.schemas.rooms import RoomExtendedResponse, RoomWithFacilitiesResponse, RoomExtendedTestResponse, RoomInfo
from src.repositories.utils import extended_room_response, extended_rooms_response
from src.schemas.facilities import FacilityResponse


class RoomsRepository(BaseRepository):
    model = RoomsModel
    # schema = RoomWithFacilitiesResponse
    schema = RoomInfo
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

    async def extended_room_response(
        self,
        date_from: date,
        date_to: date,
        room_id: int,
        hotel_id: int
    ):
        queries = extended_room_response(
            date_from=date_from,
            date_to=date_to,
            room_id=room_id,
            hotel_id=hotel_id
        )
        booked_and_avaliable_rooms_info_table = await self.session.execute(
            queries['booked_and_avaliable_rooms_info_table'])
        rooms_facilities = await self.session.execute(
            queries['room_facilities']
        )
        mapped_room_obj = (
            booked_and_avaliable_rooms_info_table.mappings().one_or_none()
        )
        mapped_room_facilities_objs = rooms_facilities.scalars().one_or_none()
        if not mapped_room_obj:
            booked_rooms = 0
            avaliable_rooms = mapped_room_facilities_objs.quantity
        else:
            booked_rooms = mapped_room_obj.booked_rooms
            avaliable_rooms = mapped_room_obj.avaliable_rooms
        if not mapped_room_facilities_objs:
            return {
                'status': 'Room with given room_id in the hotel has not found'
            }
        result = RoomExtendedTestResponse(
            room_id=mapped_room_facilities_objs.id,
            hotel_id=mapped_room_facilities_objs.hotel_id,
            title=mapped_room_facilities_objs.title,
            description=mapped_room_facilities_objs.description,
            price=mapped_room_facilities_objs.price,
            quantity=mapped_room_facilities_objs.quantity,
            booked_rooms=booked_rooms,
            avaliable_rooms=avaliable_rooms,
            facilities=mapped_room_facilities_objs.facilities
            )
        return result

    async def extended_rooms_response_manager(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )
        queries = extended_rooms_response(
            date_from=date_from,
            date_to=date_to,
            rooms_id=rooms_ids_to_get
        )
        booked_and_avaliable_rooms_info_table = await self.session.execute(
            queries['booked_and_avaliable_rooms_info_table']
        )
        rooms_facilities = await self.session.execute(
            queries['rooms_facilities']
        )
        mapped_rooms_obj = (
            booked_and_avaliable_rooms_info_table.mappings().all()
        )
        mapped_room_facilities_objs = rooms_facilities.scalars().all()
        for obj in mapped_rooms_obj:
            print(obj)
        for obj in mapped_room_facilities_objs:
            print(obj.id)
        print(mapped_rooms_obj.facilities)
        print(mapped_room_facilities_objs)