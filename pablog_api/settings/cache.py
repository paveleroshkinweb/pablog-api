from enum import StrEnum

from pablog_api.settings.base import BaseAppSettings
from pablog_api.utils.compression import CompressionType

import pydantic


class StorageType(StrEnum):
    REDIS_STORAGE: str = "REDIS_STORAGE"


class CacheSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "cache_"

    client_name: str = "PablogAPI"

    storage_type: StorageType = pydantic.Field(default=StorageType.REDIS_STORAGE)

    compression_type: CompressionType = pydantic.Field(default=CompressionType.BALANCED)

    host: str = pydantic.Field(default="127.0.0.1")

    port: int = pydantic.Field(default=6379)

    @property
    def dsn(self):
        return str(
            pydantic.RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port
            )
        )
