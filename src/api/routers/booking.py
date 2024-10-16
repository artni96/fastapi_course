from fastapi import APIRouter
from src.schemas.booking import BookingCreate, BookingResponse
from src.api.dependencies import DBDep, UserDep


booking_router = APIRouter(prefix='/bookings', tags=['Бронирование номеров'])


@booking_router.post('/')
async def create_booking(
    booking_data: BookingCreate,
    db: DBDep,
    user: UserDep
):
    result = await db.bookings.add(
        data=booking_data,
        user_id=user.id
    )
    await db.commit()
    return result
