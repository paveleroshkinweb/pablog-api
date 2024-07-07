from pablog_api.settings.base import BaseAppSettings

import pydantic


class CacheSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "redis_"

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
