from pablog_api.settings import CacheSettings

from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError


redis_cluster: None | Redis = None


async def init_redis_cluster(settings: CacheSettings):
    global redis_cluster

    redis_cluster = Redis(
        host=settings.host,
        port=settings.port,
        db=0,
        socket_keepalive=True,
        decode_responses=False,
        retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
        retry=Retry(ExponentialBackoff(), 3),
        max_connections=settings.max_connections,
        health_check_interval=10,
        socket_connect_timeout=6,
        client_name=settings.client_name,
    )

    await redis_cluster.ping()


def get_redis_cluster() -> Redis:
    if not redis_cluster:
        raise RuntimeError("Redis cluster was not initialized!")
    return redis_cluster


async def close_redis_cluster():
    if not redis_cluster:
        return
    await redis_cluster.close()
