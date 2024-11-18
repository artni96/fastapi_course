from fastapi import status
import pytest

async def test_get_bookings(auth_ac):
    result = await auth_ac.get(
        '/bookings'
    )
    assert result.status_code == 200
    isinstance(result.json(), list)


async def test_create_booking(auth_ac):
    result = await auth_ac.post(
        '/bookings',
        json={
            'room_id': 5,
            'date_to': '26.11.2024',
            'date_from': '20.11.2024'
        }
    )
    assert result.status_code == status.HTTP_201_CREATED
    result = await auth_ac.post(
        '/bookings',
        json={
            'room_id': 5,
            'date_to': '26.11.2024',
            'date_from': '20.11.2024'
        }
    )
    assert result.status_code == status.HTTP_400_BAD_REQUEST

