from functools import partial
from typing import Any

from pablog_api.memory_storage.storage import CacheStorage, KeyT, ValueT
from pablog_api.settings.cache import CacheSettings
from pablog_api.utils.compression import zlib_compression, zlib_decompression

from redis.asyncio import Redis


class RedisStorage(CacheStorage):

    def __init__(self, redis_client: Redis, settings: CacheSettings):
        self.__compressor = partial(zlib_compression, settings.compression_type)
        self.__decompressor = zlib_decompression
        self.redis_client = redis_client

    def __compress(self, value: ValueT):
        if isinstance(value, str):
            value = value.encode("UTF-8")
        return self.__compressor(value)

    async def get(self, key: KeyT) -> Any:
        data = await self.redis_client.get(key)
        return self.__decompressor(data)

    async def set(self, key: KeyT, value: ValueT, ttl_ms: None | int = None):
        compressed_data = self.__compress(value)
        await self.redis_client.set(key, compressed_data, px=ttl_ms)

    async def delete(self, *keys: KeyT):
        await self.redis_client.delete(*keys)

    async def exists(self, *keys: KeyT) -> bool:
        return await self.redis_client.exists(*keys)
