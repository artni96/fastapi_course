import pytest

from src.config import settings
from src.db import Base, engine_null_pool, engine
from src.models import *


@pytest.fixture(scope='session', autouse=True)
async def async_main():
    print(settings.MODE)
    assert settings.MODE == 'TEST'
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
