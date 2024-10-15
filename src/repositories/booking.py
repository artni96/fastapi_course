from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.schemas.booking import BookingCreate, BookingResponse
from sqlalchemy import select, insert
from src.models.rooms import RoomsModel


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = BookingResponse

    async def add(self, data: BookingCreate, user_id: int):
        price_req = select(RoomsModel.price).where(
            RoomsModel.id == data.room_id
        )
        price = await self.session.execute(price_req)
        price = price.scalars().one_or_none()
        new_booking_stmt = insert(self.model).values(
            user_id=user_id,
            price=self.model.total_cost,
            **data.model_dump()
        ).returning(self.model)
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        # return BookingResponse.model_validate(model_obj, from_attributes=True)
