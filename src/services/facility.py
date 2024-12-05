from src.exceptions import FacilityNotFoundException
from src.schemas.facilities import FacilityResponse
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_facility_by_id(
            self,
            facility_id: int,
    ) -> FacilityResponse:
        return await self.db.facilities.get_one(id=facility_id)
