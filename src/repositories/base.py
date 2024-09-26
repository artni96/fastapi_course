from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.db import engine


class BaseRepository:
    model = None

    def __init__(
            self,
            session,
    ) -> None:
        self.session = session

    async def get_all(self, pagination: PaginationDep, *args, **kwargs):
        self.limit = pagination.per_page or 3
        self.offset = (pagination.page - 1) * self.limit
        query = select(self.model)
        query = (
            query
            .offset(self.offset)
            .limit(self.limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, id):
        query = select(self.model).filter_by(id=id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, hotel):
        new_hotel_stmt = insert(self.model).values(**hotel.model_dump())
        print(new_hotel_stmt.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        new_hotel_stmt = await self.session.execute(new_hotel_stmt)
        return new_hotel_stmt.inserted_primary_key[0]