from datetime import datetime

from sqlalchemy import insert, select, update, func, desc, delete
from sqlalchemy.exc import NoResultFound

from src.exceptions import NoAvailableRoomsException, OnlyForAuthorException, BookingNotFoundException, DateToLaterThanDateFromException, \
    DateToLaterThanCurrentTimeException
from src.models import RoomsModel
from src.models.booking import BookingModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils.rooms import check_room_existence
from src.schemas.booking import BookingCreate, BookingResponse, BookingUpdate, BookingUpdateRequest, \
    BookingCreateRequest


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = BookingResponse
    mapper = BookingDataMapper
    exception = BookingNotFoundException

    async def get_all(self, offset=0, limit=3, user_id=None) -> list[BookingModel]:
        query = select(self.model)
        if user_id:
            query = query.filter_by(user_id=user_id)
        query = query.offset(offset).limit(limit).order_by(desc('created_at'))
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()
        ]

    async def add(self, booking_data: BookingCreateRequest, db, user_id: int):
        date_from = booking_data.date_from
        date_to = booking_data.date_to
        if date_to <= date_from:
            raise DateToLaterThanDateFromException
        if date_from <= datetime.today().date():
            raise DateToLaterThanCurrentTimeException
        room = await check_room_existence(room_id=booking_data.room_id, db=db)
        price = room.price
        _booking_data = BookingCreate(
            price=price, user_id=user_id, **booking_data.model_dump()
        )
        check_avaliable_rooms_amount_stmt = (
            select(
                (RoomsModel.quantity - func.coalesce(func.count("*"), 0)).label(
                    "avaliable_rooms_amount"
                )
            )
            .select_from(self.model)
            .filter(
                self.model.date_from <= _booking_data.date_to,
                self.model.date_to >= _booking_data.date_from,
                self.model.room_id == _booking_data.room_id,
            )
            .group_by(RoomsModel.quantity)
            .outerjoin(RoomsModel, RoomsModel.id == self.model.room_id)
        )
        check_avaliable_rooms_amount = await self.session.execute(
            check_avaliable_rooms_amount_stmt
        )
        check_avaliable_rooms_amount = (
            check_avaliable_rooms_amount.scalars().one_or_none()
        )
        if check_avaliable_rooms_amount is not None:
            if check_avaliable_rooms_amount <= 0:
                raise NoAvailableRoomsException()


        new_booking_stmt = (
            insert(self.model).values(**_booking_data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_obj)

    async def change(
        self, booking_data: BookingUpdateRequest, booking_id: int, user_id: int, db, exclude_unset: bool = False
    ):
        date_from = booking_data.date_from
        date_to = booking_data.date_to
        if date_to <= date_from:
            raise DateToLaterThanDateFromException
        if date_from <= datetime.today().date():
            raise DateToLaterThanCurrentTimeException
        try:
            booking = await db.bookings.get_one(id=booking_id)
            if booking:
                if booking.user_id != user_id:
                    raise OnlyForAuthorException
        except NoResultFound:
            raise BookingNotFoundException
        if booking_data.room_id:
            room = await db.rooms.get_one(id=booking_data.room_id)
        else:
            room = await db.rooms.get_one_or_none(id=booking.room_id)
        price = room.price
        _booking_data = BookingUpdate(
            price = price,
            date_from = date_from,
            date_to = date_to,
            room_id=booking_data.room_id
        )
        new_booking_stmt = (
            update(self.model)
            .where(self.model.id == booking_id)
            .values(
                **_booking_data.model_dump(exclude_none=exclude_unset), updated_at=datetime.now()
            )
            .returning(self.model)
        )

        result = await self.session.execute(new_booking_stmt)
        model_obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_obj)

    async def remove(self, booking_id: int, user_id, db):
        try:
            booking = await db.bookings.get_one(id=booking_id)
            if booking:
                if booking.user_id != user_id:
                    raise OnlyForAuthorException
        except NoResultFound:
            raise BookingNotFoundException
        removed_booking_stmt = delete(self.model).filter_by(id=booking_id)
        await self.session.execute(removed_booking_stmt)
        await db.commit()
        return {"detail": "Бронирование успешно удалено"}
