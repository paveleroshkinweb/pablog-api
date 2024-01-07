import asyncio

from pablog_api.api.server import app
from pablog_api.settings.app import get_app_settings

import pytest_asyncio

from httpx import AsyncClient


settings = get_app_settings()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    host = settings.service_settings.api_host
    port = settings.service_settings.api_port

    base_url = f"http://{host}:{port}"
    async with AsyncClient(app=app, base_url=base_url) as api_client:
        yield api_client
