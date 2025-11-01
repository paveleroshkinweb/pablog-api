from pablog_api.exception import PablogException
from pablog_api.memory_storage.redis_cluster import get_redis_cluster
from pablog_api.memory_storage.redis_storage import RedisStorage
from pablog_api.memory_storage.storage import CacheStorage
from pablog_api.settings.cache import CacheSettings, CacheStorageType


def cache_storage_factory(settings: CacheSettings) -> CacheStorage:
    storage_type = settings.storage_type
    if storage_type == CacheStorageType.REDIS_STORAGE:
        return RedisStorage(redis_client=get_redis_cluster(), settings=settings)

    raise PablogException(f"Could not initialize storage with provided type: {storage_type}")
