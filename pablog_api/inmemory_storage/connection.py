from pablog_api.settings.cache import CacheSettings

from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError


storage: None | Redis = None


async def init_in_memory_storage(cache_settings: CacheSettings, app_name: str):
    global storage

    storage = Redis(
        host=cache_settings.host,
        port=cache_settings.port,
        db=0,
        socket_keepalive=True,
        encoding="utf-8",
        decode_responses=True,
        retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
        retry=Retry(ExponentialBackoff(), 3),
        single_connection_client=True,
        health_check_interval=10,
        client_name=app_name
    )

    await storage.ping()


async def close_memory_storage():
    global storage

    if not storage:
        return

    await storage.close()
