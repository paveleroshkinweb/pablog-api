import asyncio

from pablog_api.api import app
from pablog_api.database import MasterSlaveManager, close_database, get_db_manager, init_database
from pablog_api.memory_storage import close_redis_cluster, get_redis_cluster, init_redis_cluster
from pablog_api.settings.app import get_app_settings

import pytest_asyncio

from httpx import AsyncClient
from redis.asyncio import Redis


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


@pytest_asyncio.fixture(scope="session")
async def db_manager() -> MasterSlaveManager:
    await init_database(settings.postgres, debug=False)

    db_manager = get_db_manager()

    yield db_manager

    await close_database()


@pytest_asyncio.fixture(scope="session")
async def redis_cluster() -> Redis:

    await init_redis_cluster(settings.cache)

    redis_cluster = get_redis_cluster()

    yield redis_cluster

    await close_redis_cluster()
