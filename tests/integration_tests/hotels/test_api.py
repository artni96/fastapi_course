import pytest
from fastapi import status
from datetime import date, timedelta

@pytest.mark.parametrize(
    'date_from, date_to, status',
    [
        (date.today(), date.today() + timedelta(days=4), status.HTTP_200_OK),
        (date.today()+ timedelta(days=5), date.today() + timedelta(days=4), status.HTTP_400_BAD_REQUEST)
    ]
)
async def test_get_hotels(auth_ac, date_from, date_to, status):
    result = await auth_ac.get(
        "/hotels", params={"date_from": date_from, "date_to": date_to}
    )
    assert result.status_code == status

@pytest.mark.parametrize(
    'hotel_id, status',
    [
        (1, status.HTTP_200_OK),
        (2, status.HTTP_200_OK),
        (3, status.HTTP_200_OK),
        (4, status.HTTP_404_NOT_FOUND),
    ]
)
async def test_get_hotel(ac, hotel_id, status):
    result = await ac.get(f'/hotels/{hotel_id}')
    assert result.status_code == status
