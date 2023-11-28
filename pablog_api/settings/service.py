import multiprocessing

from pablog_api.settings.base import BaseAppSettings

import pydantic


class ServiceSettings(BaseAppSettings):

    api_host: str = pydantic.Field(default="127.0.0.1")

    api_port: int = pydantic.Field(default=8001)

    workers: int = pydantic.Field(default=multiprocessing.cpu_count() * 2 + 1)

    pidfile: str = pydantic.Field(default="/var/run/pablog.pid")

    def dsn(self) -> str:
        return f'{self.api_host}:{self.api_port}'
