from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(
        self,
        session,
    ) -> None:
        self.session = session

    async def get_filtered(self, *args, **filter_by):
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        query = select(self.model).filter(*args).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model_obj)
            for model_obj in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        if model_obj is not None:
            return self.mapper.map_to_domain_entity(model_obj)

    async def add(self, data: BaseModel):
        new_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(new_data_stmt)
        new_model_obj = result.unique().scalars().one()
        return self.mapper.map_to_domain_entity(new_model_obj)

    async def add_bulk(self, data: list[BaseModel]):
        managed_data = [obj.model_dump() for obj in data]
        new_data_stmt = insert(self.model).values(managed_data)
        await self.session.execute(new_data_stmt)

    async def change(self, data: BaseModel, exclude_unset: bool = False, **filtered_by):
        query = (
            update(self.model)
            .filter_by(**filtered_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        try:
            model_obj = result.scalars().one()
            return self.mapper.map_to_domain_entity(model_obj)
        except NoResultFound:
            return {"status": "NOT FOUND"}

    async def remove(self, **filtered_by) -> dict:
        query = delete(self.model).filter_by(**filtered_by)
        result = await self.session.execute(query)
        if result.rowcount == 1:
            return {"status": "OK"}
        return {"status": "object has not been found"}
