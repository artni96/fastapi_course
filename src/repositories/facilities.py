from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesMolel, RoomFacilitiesModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import FacilityResponse, RoomFacilityAddRequest


class FacilitiesRepository(BaseRepository):
    model = FacilitiesMolel
    # schema = FacilityResponse
    mapper = FacilityDataMapper

    async def get_filtered(
        self,
        title: str
    ):
        query = select(self.model)
        if title:
            query = (
                query
                .filter(self.model.title.icontains(title))
            )
        result = await self.session.execute(query)
        # return [
        #     self.schema.model_validate(model_obj, from_attributes=True)
        #     for model_obj in result.scalars().all()
        # ]
        return [
            self.mapper.map_to_domain_entity(model_obj)
            for model_obj in result.scalars().all()
        ]


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesModel
    schema = RoomFacilityAddRequest

    async def room_facility_manager(
        self,
        room_id: int,
        new_facility_ids: list[int]
    ):
        current_facility_ids_stmt = (
            select(RoomFacilitiesModel.facility_id)
            .where(RoomFacilitiesModel.room_id == room_id)
        )
        result = await self.session.execute(current_facility_ids_stmt)
        current_facility_ids = result.scalars().all()

        facility_ids_to_delete = list(
            set(current_facility_ids) - set(new_facility_ids))
        facility_ids_to_add = list(
            set(new_facility_ids) - set(current_facility_ids)
        )
        facility_ids_to_add = [
            RoomFacilityAddRequest(room_id=room_id, facility_id=facility_id)
            for facility_id in facility_ids_to_add
        ]
        if facility_ids_to_delete:
            query_to_delete = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(
                        facility_ids_to_delete))
            )
            await self.session.execute(query_to_delete)
        if facility_ids_to_add:
            managed_facility_data = [
                obj.model_dump() for obj in facility_ids_to_add]
            facility_ids_to_add = (
                insert(self.model)
                .values(managed_facility_data)
            )
            await self.session.execute(facility_ids_to_add)
