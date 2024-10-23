from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from sqlalchemy import insert, select, update
from src.utils.rooms import check_room_existence
from datetime import datetime
from src.db import engine


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = BookingResponse
    mapper = BookingDataMapper

    async def get_all(
            self,
            offset=0,
            limit=3,
            user_id=None
    ) -> list[BookingModel]:
        query = select(self.model)
        if user_id:
            query = query.filter_by(user_id=user_id)
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        # return [
        #     self.schema.model_validate(hotel, from_attributes=True)
        #     for hotel in result.scalars().all()
        # ]
        return [
            self.mapper.map_to_domain_entity(hotel)
            for hotel in result.scalars().all()
        ]

    async def add(self, data: BookingCreate):
        new_booking_stmt = insert(self.model).values(
            **data.model_dump()
        ).returning(self.model)
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        # return self.schema.model_validate(model_obj, from_attributes=True)
        return self.mapper.map_to_domain_entity(model_obj)

    async def change(
            self,
            data: BookingUpdate,
            booking_id: int,
            exclude_unset: bool = False):
        if data.room_id:
            if not await check_room_existence(
                room_id=data.room_id,
                session=self.session
            ):
                return {'status': 'room with given room_id has not been found'}
        new_booking_stmt = (
            update(self.model)
            .where(self.model.id == booking_id)
            .values(
                **data.model_dump(exclude_none=exclude_unset),
                updated_at=datetime.now())
            .returning(self.model)
        )
        print(new_booking_stmt.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        # return self.schema.model_validate(model_obj, from_attributes=True)
        return self.mapper.map_to_domain_entity(model_obj)