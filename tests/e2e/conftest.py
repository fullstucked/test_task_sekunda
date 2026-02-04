
import pytest
import httpx
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from setup.app_factory import create_app
from infra.db.base import Base

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
        # rollback everything the test did
        await session.rollback()

@pytest.fixture
async def client(db_session):
    app = create_app()

    async def override_get_db():
        yield db_session

    app.dependency_overrides = {}
    app.dependency_overrides[
        "infra.db.dependency.get_db"
    ] = override_get_db

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

