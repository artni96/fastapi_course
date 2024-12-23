from datetime import date, timedelta

from src.schemas.booking import BookingCreate, BookingUpdate, BookingCreateRequest, BookingUpdateRequest
import pytest


@pytest.mark.order(1)
async def test_booking_crud(db, add_new_user, setup_database):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    # print(room_id)
    initial_booking_data = BookingCreateRequest(
        room_id=room_id,
        date_from=date.today() + timedelta(days=1),
        date_to=date.today() + timedelta(days=5),
    )
    new_booking = await db.bookings.add(booking_data=initial_booking_data, db=db, user_id=user_id)
    assert new_booking.user_id == user_id
    assert new_booking.room_id == initial_booking_data.room_id
    get_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert get_booking.user_id == user_id
    assert get_booking.room_id == initial_booking_data.room_id
    updated_booking_data = BookingUpdateRequest(
        date_from=date.today() + timedelta(days=3),
        date_to=date.today() + timedelta(days=6),
        room_id=room_id
    )
    updated_booking = await db.bookings.change(
        booking_id=get_booking.id, booking_data=updated_booking_data, exclude_unset=True, db=db, user_id=user_id
    )
    assert updated_booking.user_id == user_id
    assert updated_booking.room_id == initial_booking_data.room_id
    assert updated_booking.date_from == updated_booking_data.date_from
    assert updated_booking.date_to == updated_booking_data.date_to
    await db.bookings.remove(booking_id=updated_booking.id, user_id=user_id, db=db)
    all_bookings = await db.bookings.get_all()
    assert all_bookings == []
    await db.rollback()
