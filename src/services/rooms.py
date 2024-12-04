from datetime import date

from src.exceptions import HotelNotFoundException, RoomNotFoundException, RoomForHotelNotFoundException
from src.repositories.utils.facilities import check_facilities_existence
from src.schemas.facilities import RoomFacilityAddRequest
from src.schemas.rooms import RoomCreateRequest, RoomCreate, RoomInfo, RoomPutRequest, RoomPut, RoomPatchRequest, \
    RoomPatch
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_hotel_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms = await self.db.rooms.get_rooms_by_date(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms

    async def get_hotel_room(
        self,
        hotel_id: int,
        room_id: int
    ):
        return await self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)



    async def create_room(
        self,
        hotel_id: int,
        room_data: RoomCreateRequest
    ):
        # try:
        await self.db.hotels.get_one(id=hotel_id)
        # except HotelNotFoundException as ex:
        #     raise HotelNotFoundException from ex
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
        _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
        room: RoomInfo = await self.db.rooms.add(data=_room_data)
        if room_data.facility_ids:
            await check_facilities_existence(db=self.db, facility_ids=room_data.facility_ids)
            facility_ids = [
                RoomFacilityAddRequest(room_id=room.id, facility_id=facility_id)
                for facility_id in room_data.facility_ids
            ]
            await self.db.room_facilities.add_bulk(data=facility_ids)

        await self.db.commit()
        return await self.db.rooms.get_one_or_none(id=room.id)

    async def remove_hotel_room(self, hotel_id: int, room_id: int):
        result = await self.db.rooms.remove(hotel_id=hotel_id, id=room_id)
        await self.db.commit()
        return result

    async def update_hotel_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPutRequest
    ):
        new_facility_ids = set(room_data.facility_ids)
        await check_facilities_existence(db=self.db, facility_ids=new_facility_ids)
        _room_data = RoomPut(hotel_id=hotel_id, **room_data.model_dump())
        result = await self.db.rooms.change(
            id=room_id, hotel_id=hotel_id, data=_room_data, exclude_unset=False
        )
        await self.db.room_facilities.room_facility_creator(
            room_id=room_id, new_facility_ids=new_facility_ids
        )
        await self.db.commit()
        return result

    async def update_hotel_room_partially(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
    ):
        _room_data = RoomPatch(
            hotel_id=hotel_id,
            **room_data.model_dump(exclude_unset=True, exclude="facility_ids"),
        )
        if room_data.facility_ids:
            new_facility_ids = set(room_data.facility_ids)
            await check_facilities_existence(db=self.db, facility_ids=new_facility_ids)
        result = await self.db.rooms.change(
            id=room_id, hotel_id=hotel_id, data=_room_data, exclude_unset=True
        )
        if room_data.facility_ids:
            new_facility_ids = set(room_data.facility_ids)
            await check_facilities_existence(db=self.db, facility_ids=new_facility_ids)
            if new_facility_ids:
                await self.db.room_facilities.room_facility_creator(
                    room_id=room_id, new_facility_ids=new_facility_ids
                )
        await self.db.commit()
        return result

    async def get_rooms_with_ext_info_by_date(
        self,
        date_from: date,
        date_to: date,
        hotel_id: int,
        room_id: int,
    ):
        return await self.db.rooms.extended_room_response(
            date_from=date_from, date_to=date_to, room_id=room_id, hotel_id=hotel_id
        )
