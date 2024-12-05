from src.exceptions import FacilityNotFoundException
from src.schemas.facilities import FacilityResponse, FacilityBaseRequest
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_facility_by_id(
            self,
            facility_id: int,
    ) -> FacilityResponse:
        return await self.db.facilities.get_one(id=facility_id)

    async def get_all_facilities(
        self,
        title: str | None = None
    ) -> list[FacilityResponse]:
        return await self.db.facilities.get_filtered(title=title)

    async def create_facility(
        self,
        facility_data: FacilityBaseRequest
    ) -> FacilityResponse:
        new_facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return new_facility

    async def update_facility(
        self,
        facility_id: int,
        facility_data: FacilityBaseRequest
    ) -> FacilityResponse:
        updated_facility = await self.db.facilities.change(id=facility_id, data=facility_data)
        await self.db.commit()
        return updated_facility

    async def delete_facility(self, facility_id: int) -> dict:
        result = await self.db.facilities.remove(id=facility_id)
        await self.db.commit()
        return result
