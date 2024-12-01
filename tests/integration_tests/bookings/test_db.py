from datetime import date

from src.schemas.booking import BookingCreate, BookingUpdate
import pytest


@pytest.mark.order(1)
async def test_booking_crud(db, add_new_user, setup_database):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    initial_booking_data = BookingCreate(
        price=1200,
        user_id=user_id,
        room_id=room_id,
        date_to=date(year=2024, month=11, day=20),
        date_from=date(year=2024, month=11, day=16),
    )
    new_booking = await db.bookings.add(data=initial_booking_data)
    assert new_booking.price == initial_booking_data.price
    assert new_booking.user_id == initial_booking_data.user_id
    assert new_booking.room_id == initial_booking_data.room_id
    get_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert get_booking.price == initial_booking_data.price
    assert get_booking.user_id == initial_booking_data.user_id
    assert get_booking.room_id == initial_booking_data.room_id
    updated_booking_data = BookingUpdate(
        price=2400,
        date_to=date(year=2024, month=11, day=20),
        date_from=date(year=2024, month=11, day=16),
    )
    updated_booking = await db.bookings.change(
        booking_id=get_booking.id, data=updated_booking_data, exclude_unset=True
    )
    assert updated_booking.price == updated_booking_data.price
    assert updated_booking.user_id == initial_booking_data.user_id
    assert updated_booking.room_id == initial_booking_data.room_id
    assert updated_booking.date_from == updated_booking_data.date_from
    assert updated_booking.date_to == updated_booking_data.date_to
    await db.bookings.remove(id=updated_booking.id)
    all_bookings = await db.bookings.get_all()
    assert all_bookings == []
    await db.rollback()
