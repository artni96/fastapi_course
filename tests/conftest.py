import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.db import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels import HotelAddPut
from src.schemas.rooms import RoomCreate
from src.utils.db_manager import DBManager


@pytest.fixture(scope='session', autouse=True)
async def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(autouse=True)
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield  db

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        with open('tests/mock_hotels.json', 'r') as f:
            hotels_json = json.load(f)
        hotels_data = [HotelAddPut.model_validate(hotel) for hotel in hotels_json]
        with open('tests/mock_rooms.json', 'r') as f:
            rooms_json = json.load(f)
        rooms_data = [RoomCreate.model_validate(room) for room in rooms_json]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.hotels.add_bulk(hotels_data)
        await _db.rooms.add_bulk(rooms_data)
        await _db.commit()


@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope='session', autouse=True)
async def add_new_user(ac, setup_database):
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
