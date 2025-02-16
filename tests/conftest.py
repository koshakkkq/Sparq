import pytest
import pytest_asyncio

import sqlalchemy
from sqlalchemy.pool import NullPool
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from app.main import get_application
from app.config.settings import settings
from app.database.helper import get_db_session


@pytest_asyncio.fixture
async def async_engine():
    async_engine = create_async_engine(
        settings.database_url,
        poolclass=NullPool,
    )

    yield async_engine
    await async_engine.dispose()


@pytest.fixture
def app():
    return get_application()


@pytest_asyncio.fixture
async def db_session(async_engine):
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()

        async_session = AsyncSession(conn)

        @sqlalchemy.event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return

            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield async_session

        await conn.rollback()
    await async_engine.dispose()


@pytest_asyncio.fixture
async def test_client(db_session, app):
    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    yield AsyncClient(app=app, base_url="http://testserver")
