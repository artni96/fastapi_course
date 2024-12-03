import pytest
from datetime import date, timedelta
from fastapi import status


@pytest.mark.parametrize(
    'hotel_id, date_from, date_to, status',
    [
        (1, date.today() + timedelta(days=1), date.today() + timedelta(days=3), status.HTTP_200_OK),
        (1, date.today() + timedelta(days=5), date.today() + timedelta(days=3), status.HTTP_400_BAD_REQUEST)
    ]
)
async def test_rooms_by_date(ac, hotel_id, date_from, date_to, status):
    get_rooms = await ac.get(
        f'/hotels/{hotel_id}/rooms',
        params={"date_from": date_from, "date_to": date_to}
    )
    assert get_rooms.status_code == status, f'значение status отличается от {status}'
