from sqlalchemy.exc import NoResultFound

from src.exceptions import OnlyForAuthorException, BookingNotFoundException
from src.schemas.booking import BookingCreateRequest, BookingUpdateRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self, pagination):
        per_page = pagination.per_page or 3
        bookings = await self.db.bookings.get_all(
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
        return bookings

    async def get_my_bookings(self, user, pagination):
        per_page = pagination.per_page or 3
        bookings = await self.db.bookings.get_all(
            limit=per_page, offset=per_page * (pagination.page - 1), user_id=user.id
        )
        return bookings

    async def create_booking(
            self,
            booking_data: BookingCreateRequest,
            user
    ):
        result = await self.db.bookings.add(booking_data=booking_data, user_id=user.id, db=self.db)
        await self.db.commit()
        return result

    async def update_booking(
        self,
        booking_id: int,
        user,
        booking_data: BookingUpdateRequest,
    ):
        return await self.db.bookings.change(
            booking_data=booking_data,
            exclude_unset=True,
            booking_id=booking_id,
            db=self.db,
            user_id=user.id
        )

    async def remove_booking(self, booking_id: int, user):
        return await self.db.bookings.remove(db=self.db, booking_id=booking_id, user_id=user.id)
