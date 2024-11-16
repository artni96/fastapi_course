import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.models import *
from src.db import Base, engine_null_pool
from src.config import settings
from src.main import app


@pytest.fixture(scope='session', autouse=True)
async def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    print(settings.DB_NAME)
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async  def hotels_setup(setup_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        with open('tests/mock_hotels.json', 'r') as f:
            hotels_json = json.load(f)
            for hotel in hotels_json:
                new_hotel = await ac.post(
                    "/hotels/",
                    json=hotel
                )
                assert  new_hotel.status_code == 201

@pytest.fixture(scope='session', autouse=True)
async  def rooms_setup(hotels_setup):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        with open('tests/mock_rooms.json', 'r') as f:
            rooms_json = json.load(f)
            for room in rooms_json:
                new_room = await ac.post(
                    f"/hotels/{room['hotel_id']}",
                    json=room,
                )
                assert  new_room.status_code == 201


@pytest.fixture(scope='session', autouse=True)
async def add_new_user(setup_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/auth/register",
            json = {
                "email": "user@example.com",
                "password": "string",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "username": "string",
                "first_name": "string",
                "last_name": "string"
            })
    assert response.status_code == 201
    # assert response.json() == {"message": "Tomato"}
