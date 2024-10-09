from pydantic import BaseModel
from sqlalchemy import insert, select, delete, update

from src.api.dependencies import PaginationDep
from sqlalchemy.exc import NoResultFound


class BaseRepository:
    model = None
    schema: BaseModel = None

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
        return [
            self.schema.model_validate(model_obj, from_attributes=True)
            for model_obj in result.scalars().all()
        ]

    async def get_one_or_none(self, id):
        query = select(self.model).filter_by(id=id)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        if result is not None:
            return self.schema.model_validate(
                model_obj, from_attributes=True
            )
        return {'status': 'NOT FOUND'}

    async def add(self, data: BaseModel):
        new_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(
                self.model
            )
        )
        result = await self.session.execute(new_data_stmt)
        new_model_obj = result.scalars().one()
        return self.schema.model_validate(
            new_model_obj,
            from_attributes=True)

    async def change(
            self,
            data: BaseModel,
            exclude_unset: bool = False,
            **filtered_by
    ):
        query = (
            update(self.model)
            .filter_by(**filtered_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        try:
            model_obj = result.scalars().one()
            return self.schema.model_validate(model_obj, from_attributes=True)
        except NoResultFound:
            return {'status': 'NOT FOUND'}

    async def remove(self, **filtered_by):
        query = delete(self.model).filter_by(**filtered_by)
        result = await self.session.execute(query)
        if result.rowcount == 1:
            return {'status': 'OK'}
        return {'status': 'Unprocessable Entity'}
