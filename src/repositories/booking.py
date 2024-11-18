from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import insert, select, update, func

from src.models import RoomsModel
from src.models.booking import BookingModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils.rooms import check_room_existence
from src.schemas.booking import BookingCreate, BookingResponse, BookingUpdate


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
        return [
            self.mapper.map_to_domain_entity(hotel)
            for hotel in result.scalars().all()
        ]

    async def add(self, data: BookingCreate):
        check_avaliable_rooms_amount_stmt = (
            select((RoomsModel.quantity - func.coalesce(func.count('*'), 0)).label('avaliable_rooms_amount'))
            .select_from(self.model)
            .filter(
                self.model.date_from <= data.date_to,
                self.model.date_to >= data.date_from,
                self.model.room_id == data.room_id
            )
            .group_by(RoomsModel.quantity)
            .outerjoin(
                RoomsModel,
                RoomsModel.id == self.model.room_id
            )
        )
        check_avaliable_rooms_amount = await self.session.execute(
            check_avaliable_rooms_amount_stmt
        )
        check_avaliable_rooms_amount = check_avaliable_rooms_amount.scalars().one_or_none()
        if check_avaliable_rooms_amount is not None:
            if check_avaliable_rooms_amount <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Нет свободных номеров')
        new_booking_stmt = insert(self.model).values(
            **data.model_dump()
        ).returning(self.model)
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_obj)

    async def change(
        self,
        data: BookingUpdate,
        booking_id: int,
        exclude_unset: bool = False
    ):
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
        # print(new_booking_stmt.compile(
        #     engine,
        #     compile_kwargs={"literal_binds": True})
        # )
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_obj)
