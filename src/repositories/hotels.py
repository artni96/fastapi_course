from sqlalchemy import select
from models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.api.dependencies import PaginationDep


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            title,
            location,
            offset,
            limit
    ):
        query = select(self.model)
        if title:
            query = query.filter(self.model.title.icontains(title))
        if location:
            query = query.filter(self.model.location.icontains(location))
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
