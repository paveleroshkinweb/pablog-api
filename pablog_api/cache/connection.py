from pablog_api.settings.cache import CacheSettings

from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError


cache_client: None | Redis = None


async def init_cache(cache_settings: CacheSettings, app_name: str):
    global cache_client

    cache_client = Redis(
        host=cache_settings.host,
        port=cache_settings.port,
        db=0,
        socket_keepalive=True,
        encoding="utf-8",
        decode_responses=True,
        retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
        retry=Retry(ExponentialBackoff(), 3),
        single_connection_client=True,
        health_check_interval=7,
        client_name=app_name
    )

    await cache_client.ping()
