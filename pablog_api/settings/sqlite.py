from pablog_api.settings.base import BaseAppSettings

import pydantic


class SQLiteSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "sqlite_"

    url: str = pydantic.Field(default="sqlite+aiosqlite:////var/db/pablog.db")

    busy_timeout: int = pydantic.Field(default=5000)

    @property
    def dsn(self) -> str:
        return self.url
