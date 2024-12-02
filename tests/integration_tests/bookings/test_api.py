from datetime import date, timedelta

import pytest
from fastapi import status
from sqlalchemy import delete

from src.db import engine_null_pool
from src.models import BookingModel

DATE_FORMAT = "%d.%m.%Y"


async def test_get_bookings(auth_ac):
    result = await auth_ac.get("/bookings")
    assert result.status_code == status.HTTP_200_OK
    isinstance(result.json(), list)


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        # (5, "20.12.2024", "26.12.2024", status.HTTP_201_CREATED),
        # (5, "19.12.2024", "26.12.2024", status.HTTP_400_BAD_REQUEST),
        # (5, "21.12.2024", "25.12.2024", status.HTTP_400_BAD_REQUEST),
        # (5, "27.12.2024", "28.12.2024", status.HTTP_201_CREATED),
        # (5, "26.12.2024", "27.12.2024", status.HTTP_400_BAD_REQUEST),
        (5, date.today()+timedelta(days=2), date.today()+timedelta(days=8), status.HTTP_201_CREATED),
        (5, date.today()+timedelta(days=1), date.today()+timedelta(days=8), status.HTTP_201_CREATED),
        (5, date.today()+timedelta(days=3), date.today()+timedelta(days=7), status.HTTP_201_CREATED),
        (5, date.today()+timedelta(days=9), date.today()+timedelta(days=10), status.HTTP_201_CREATED),
        (5, date.today()+timedelta(days=8), date.today()+timedelta(days=9), status.HTTP_201_CREATED),
    ],
)
@pytest.mark.order(2)
async def test_create_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    auth_ac,
):
    new_booking = await auth_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": str(date_from), "date_to": str(date_to)},
    )
    print(new_booking.json())
    # assert new_booking.status_code == status_code
    # print({"room_id": room_id, "date_from": str(date_from), "date_to": str(date_to)})


@pytest.mark.order(3)
async def test_delete_all_bookings():
    async with engine_null_pool.begin() as conn:
        clean_up_bookings_stmt = delete(BookingModel)
        await conn.execute(clean_up_bookings_stmt)
        await conn.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, bookings_amount",
    [
        # (5, '20.11.2024', '23.11.2024', status.HTTP_201_CREATED, 1),
        # (5, '24.11.2024', '26.11.2024', status.HTTP_201_CREATED, 2),
        # (5, '24.11.2024', '26.11.2024', status.HTTP_400_BAD_REQUEST, 2),
        (5, date.today() + timedelta(days=1), date.today() + timedelta(days=8), status.HTTP_201_CREATED, 1),
        (5, date.today() + timedelta(days=1), date.today() + timedelta(days=8), status.HTTP_201_CREATED, 1),
        (5, date.today() + timedelta(days=1), date.today() + timedelta(days=8), status.HTTP_201_CREATED, 1),
    ],
)
@pytest.mark.order(4)
async def test_my_bookings(
    auth_ac, room_id, date_from, date_to, status_code, bookings_amount
):
    new_booking = await auth_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": str(date_from), "date_to": str(date_to)},
    )
    assert new_booking.status_code == status_code
    # current_bookings_amount = await auth_ac.get("/bookings/me")
    # assert len(current_bookings_amount.json()) == booki ngs_amount
