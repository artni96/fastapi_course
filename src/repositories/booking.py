from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.schemas.booking import BookingCreate, BookingResponse
from sqlalchemy import insert, select, update
from src.utils.rooms import check_room_existence
from datetime import datetime


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = BookingResponse

    async def get_all(self, offset=0, limit=3, user_id=None):
        query = select(self.model)
        if user_id:
            query = query.filter_by(user_id=user_id)
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]

    async def add(self, data: BookingCreate):
        if not await check_room_existence(
            room_id=data.room_id,
            session=self.session
        ):
            return {'status': 'room with given room_id has not been found'}
        new_booking_stmt = insert(self.model).values(
            **data.model_dump()
        ).returning(self.model)
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.schema.model_validate(model_obj, from_attributes=True)

    async def change(
            self,
            data: BookingCreate,
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
                **data.model_dump(exclude_unset=exclude_unset),
                updated_at=datetime.now())
            .returning(self.model)
        )
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.schema.model_validate(model_obj, from_attributes=True)
