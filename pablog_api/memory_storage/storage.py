from abc import ABC, abstractmethod
from functools import partial

from pablog_api.memory_storage.exception import MemoryStorageNotSupportedException
from pablog_api.memory_storage.redis_cluster import get_redis_cluster
from pablog_api.settings.cache import CacheSettings, CacheStorageType
from pablog_api.utils.compression import zlib_compression, zlib_decompression

from redis.asyncio import Redis


KeyT = bytes | str | memoryview
ValueT = bytes | memoryview | str


class CacheStorage(ABC):

    @abstractmethod
    async def get(self, key: KeyT) -> bytes | None:
        pass

    @abstractmethod
    async def set(self, key: KeyT, value: ValueT, ttl_ms: None | int = None) -> None:
        pass

    @abstractmethod
    async def delete(self, *keys: KeyT) -> None:
        pass

    @abstractmethod
    async def exists(self, *keys: KeyT) -> bool:
        pass


class RedisStorage(CacheStorage):

    def __init__(self, redis_client: Redis, settings: CacheSettings):
        self.__compressor = partial(zlib_compression, settings.compression_type)
        self.__decompressor = zlib_decompression
        self.redis_client = redis_client

    def __compress(self, value: ValueT) -> bytes:
        if isinstance(value, str):
            value = value.encode("UTF-8")
        return self.__compressor(value)

    async def get(self, key: KeyT) -> bytes | None:
        data = await self.redis_client.get(key)
        if not data:
            return None
        return self.__decompressor(data)

    async def set(self, key: KeyT, value: ValueT, ttl_ms: None | int = None) -> None:
        compressed_data = self.__compress(value)
        await self.redis_client.set(key, compressed_data, px=ttl_ms)

    async def delete(self, *keys: KeyT) -> None:
        await self.redis_client.delete(*keys)

    async def exists(self, *keys: KeyT) -> bool:
        return await self.redis_client.exists(*keys)


def memory_storage_factory(settings: CacheSettings) -> CacheStorage:
    storage_type = settings.storage_type
    if storage_type == CacheStorageType.REDIS_STORAGE:
        return RedisStorage(redis_client=get_redis_cluster(), settings=settings)

    raise MemoryStorageNotSupportedException
