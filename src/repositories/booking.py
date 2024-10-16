from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.schemas.booking import BookingCreate, BookingResponse
from sqlalchemy import select, insert
from src.models.rooms import RoomsModel
from src.utils.rooms import check_room_existence


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = BookingResponse

    async def add(self, data: BookingCreate, user_id: int):
        price_req = select(RoomsModel.price).where(
            RoomsModel.id == data.room_id
        )
        price = await self.session.execute(price_req)
        price = price.scalars().one_or_none()
        if not await check_room_existence(
            room_id=data.room_id,
            session=self.session
        ):
            return {'status': 'room with given room_id has not been found'}
        new_booking_stmt = insert(self.model).values(
            user_id=user_id,
            price=price,
            **data.model_dump()
        ).returning(self.model)
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.schema.model_validate(model_obj, from_attributes=True)
