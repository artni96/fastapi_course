from sqlalchemy import delete, insert, select, update

from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomBase, RoomInfo
from src.db import engine
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomInfo

    async def get_all(self, hotel_id: int) -> list[RoomInfo]:
        query = select(self.model).where(hotel_id == hotel_id)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(room, from_attributes=True)
            for room in result.scalars().all()
        ]

    async def add(
            self,
            hotel_id: int,
            room_data: RoomBase
    ) -> RoomInfo:
        query = insert(self.model).values(
            **room_data.model_dump(), hotel_id=hotel_id).returning(self.model)
        result = await self.session.execute(query)
        model_obj = result.scalars().one()
        return self.schema.model_validate(model_obj, from_attributes=True)

    async def get_one_or_none(
            self,
            hotel_id: int,
            room_id: int
    ) -> RoomInfo:
        query = select(self.model).filter_by(
            hotel_id=hotel_id, id=room_id)
        result = await self.session.execute(query)
        model_obj = result.scalars().one_or_none()
        return self.schema.model_validate(model_obj, from_attributes=True)

    async def remove(
            self,
            hotel_id: int,
            room_id: int
    ):
        query = delete(self.model).filter_by(
            hotel_id=hotel_id, id=room_id)
        result = await self.session.execute(query)
        if result.rowcount == 1:
            return {'status': 'NO CONTENT'}
        return {'status': 'NOT FOUND'}

    async def change(
            self,
            hotel_id: int,
            room_id: int,
            room_data: BaseModel,
            exclude_unset: bool = False
    ):
        query = (
            update(self.model)
            .filter_by(id=room_id, hotel_id=hotel_id)
            .values(**room_data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        print(query.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        result = await self.session.execute(query)
        try:
            model_obj = result.scalars().one()
            return self.schema.model_validate(model_obj, from_attributes=True)
        except NoResultFound:
            return {'status': 'NOT FOUND'}
