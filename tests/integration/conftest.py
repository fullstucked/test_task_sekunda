import asyncio
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from infra.db.base import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    url = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    engine = create_async_engine(url, echo=False, future=True)

    Base.metadata.bind = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    )

    async with async_session() as session:
        yield session
        await session.rollback()
