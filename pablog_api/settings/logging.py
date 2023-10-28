import logging
import time

from enum import Enum, unique
from typing import Any

from pablog_api.settings.base import BaseAppSettings
from pablog_api.settings.code_environment import CodeEnvironment

import pydantic


# Log time in UTC
logging.Formatter.converter = time.gmtime


@unique
class LoggerLevelType(str, Enum):
    CRITICAL: str = "CRITICAL"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"
    INFO: str = "INFO"
    DEBUG: str = "DEBUG"


class LoggingSettings(BaseAppSettings):
    log_level: LoggerLevelType = pydantic.Field(default=LoggerLevelType.INFO)

    def get_config(self, environment: CodeEnvironment = CodeEnvironment.DEV) -> dict[str, Any]:
        return {}
