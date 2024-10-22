from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesMolel
from src.schemas.facilities import FacilityResponse
from sqlalchemy import select


class FacilitiesRepository(BaseRepository):
    model = FacilitiesMolel
    schema = FacilityResponse

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
        return [
            self.schema.model_validate(model_obj, from_attributes=True)
            for model_obj in result.scalars().all()
        ]
