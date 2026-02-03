import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    url=os.getenv("DATABASE_URL"),
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session():
    try:
        async with SessionLocal() as session:
            yield session
    except Exception as e:
        raise e
