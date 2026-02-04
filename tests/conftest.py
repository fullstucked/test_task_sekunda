import asyncio

import pytest

pytest_plugins = ("pytest_asyncio",)
@pytest.fixture(scope="session")
def event_loop():
    """
    Use a single event loop for the entire test session.
    Required for async domain services or async repositories.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

