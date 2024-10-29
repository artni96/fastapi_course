from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesMolel, RoomFacilitiesModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import RoomFacilityAddRequest


class FacilitiesRepository(BaseRepository):
    model = FacilitiesMolel
    mapper = FacilityDataMapper

    async def get_filtered(
        self,
        title: str | None = None
    ):
        query = select(self.model)
        if title:
            query = (
                query
                .filter(self.model.title.icontains(title))
            )
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model_obj)
            for model_obj in result.scalars().all()
        ]

    async def get_by_ids(
        self,
        ids: list[int]
    ):
        query = select(self.model).filter(self.model.id.in_(ids))
        result = await self.session.execute(query)
        scalared_result = result.scalars().all()
        return scalared_result

    async def get_all(self, *args, **kwargs):
        query = select(self.model).select_from(self.model)
        result = await self.session.execute(query)
        return [
            (f"id: {(obj.__dict__)['id']}, title: {(obj.__dict__)['title']}")
            for obj in result.scalars().all()]


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesModel
    schema = RoomFacilityAddRequest

    async def room_facility_creator(
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
