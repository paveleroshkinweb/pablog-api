import multiprocessing

from pablog_api.settings.base import BaseAppSettings

import pydantic


class ServiceSettings(BaseAppSettings):

    api_host: str

    api_port: int

    workers: int = pydantic.Field(default=multiprocessing.cpu_count() * 2 + 1)

    def dsn(self) -> str:
        return f'{self.api_host}:{self.api_port}'
