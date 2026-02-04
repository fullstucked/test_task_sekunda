import asyncio
import os
import pathlib
import sys

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

project_roots = ["/app", "/app/src", "/src", "/src/handbook"]
for root in project_roots:
    if root not in sys.path:
        sys.path.insert(0, root)
config = context.config

from src.handbook.infra.db import Base

target_metadata = Base.metadata

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_async_engine(
        os.getenv("DATABASE_URL"), echo=False, future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
