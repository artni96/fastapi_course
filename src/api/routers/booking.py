from fastapi import APIRouter
from src.schemas.booking import BookingCreateRequest, BookingCreate
from src.api.dependencies import DBDep, PaginationDep, UserDep


booking_router = APIRouter(prefix='/bookings', tags=['Бронирование номеров'])


@booking_router.post('/')
async def create_booking(
    booking_data: BookingCreateRequest,
    db: DBDep,
    user: UserDep
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price = room.price
    _booking_data = BookingCreate(
        price=price,
        user_id=user.id,
        **booking_data.model_dump()
    )
    result = await db.bookings.add(
        data=_booking_data
    )
    await db.commit()
    return result


@booking_router.get('/')
async def get_all_bookings(
    db: DBDep,
    user: UserDep,
    pagination: PaginationDep
):
    per_page = pagination.per_page or 3
    bookings = await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )
    return bookings


@booking_router.get('/me')
async def get_my_bookings(
    db: DBDep,
    user: UserDep,
    pagination: PaginationDep
):
    per_page = pagination.per_page or 3
    bookings = await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        user_id=user.id
    )
    return bookings
