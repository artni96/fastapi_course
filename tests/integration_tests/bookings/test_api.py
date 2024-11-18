from dns.resolver import query
from fastapi import status
import pytest

from src.db import engine_null_pool, Base
from src.models import BookingModel
from sqlalchemy import text
from sqlalchemy import delete



async def test_get_bookings(auth_ac):
    result = await auth_ac.get(
        '/bookings'
    )
    assert result.status_code == status.HTTP_200_OK
    isinstance(result.json(), list)


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (5, '20.11.2024', '26.11.2024', status.HTTP_201_CREATED),
        (5, '19.11.2024', '26.11.2024', status.HTTP_400_BAD_REQUEST),
        (5, '21.11.2024', '25.11.2024', status.HTTP_400_BAD_REQUEST),
        (5, '27.11.2024', '28.11.2024', status.HTTP_201_CREATED),
        (5, '26.11.2024', '27.11.2024', status.HTTP_400_BAD_REQUEST),
    ]
)
@pytest.mark.order(2)
async def test_create_booking(
    auth_ac,
    room_id,
    date_from,
    date_to,
    status_code
):
    new_booking = await auth_ac.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to
        }
    )
    assert new_booking.status_code == status_code


@pytest.mark.order(3)
async def test_delete_all_bookings():
    async with engine_null_pool.begin() as conn:
        clean_up_bookings_stmt = delete(BookingModel)
        await conn.execute(clean_up_bookings_stmt)
        await conn.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, bookings_amount",
    [
        (5, '20.11.2024', '23.11.2024', status.HTTP_201_CREATED, 1),
        (5, '24.11.2024', '26.11.2024', status.HTTP_201_CREATED, 2),
        (5, '24.11.2024', '26.11.2024', status.HTTP_400_BAD_REQUEST, 2),
    ]
)
@pytest.mark.order(4)
async def test_my_bookings(
    auth_ac,
    room_id,
    date_from,
    date_to,
    status_code,
    bookings_amount
):
    new_booking = await auth_ac.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to
        }
    )
    assert new_booking.status_code == status_code
    current_bookings_amount = await auth_ac.get(
        '/bookings/me'
    )
    assert len(current_bookings_amount.json()) == bookings_amount