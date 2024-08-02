import os

from functools import lru_cache

from pablog_api.settings.base import BaseAppSettings
from pablog_api.settings.cache import CacheSettings
from pablog_api.settings.code_environment import CodeEnvironment
from pablog_api.settings.logging import LoggingSettings
from pablog_api.settings.postgres import PostgresSettings
from pablog_api.settings.service import ServiceSettings

import pydantic


def _read_version() -> str:
    cwd = os.getcwd()
    version_file = os.path.join(cwd, "VERSION")
    with open(version_file) as file:
        return file.readline().strip()


class AppSettings(BaseAppSettings):

    app_name: str = "PablogAPI"
    app_version: str = _read_version()

    enable_stats: bool = pydantic.Field(default=False)
    environment: CodeEnvironment = pydantic.Field(default=CodeEnvironment.DEV)
    service_settings: ServiceSettings = ServiceSettings()
    logging: LoggingSettings = LoggingSettings()
    postgres: PostgresSettings = PostgresSettings()
    cache: CacheSettings = CacheSettings()

    def is_development(self) -> bool:
        return self.environment == CodeEnvironment.DEV


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()
