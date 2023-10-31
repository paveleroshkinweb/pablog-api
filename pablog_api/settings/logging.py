import logging
import os
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


def get_dev_config(log_level: LoggerLevelType, log_file_path: str) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default"
            },
            "file": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.FileHandler",
                "mode": "a",
                "encoding": "UTF-8",
                "filename": log_file_path,
                "formatter": "default",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": log_level.value
            },
            "uvicorn.error": {
                "handlers": ["console", "file"],
                "level": log_level.value,
                "propagate": False
            },
        }
    }
    return config


class LoggingSettings(BaseAppSettings):

    log_level: LoggerLevelType = pydantic.Field(default=LoggerLevelType.INFO)

    log_file_path: str = pydantic.Field(default=os.path.join(os.getcwd(), "logs", "pablog.logs"))

    def get_config(self, environment: CodeEnvironment = CodeEnvironment.DEV) -> dict[str, Any]:
        if environment == CodeEnvironment.DEV:
            return get_dev_config(self.log_level, self.log_file_path)
        raise ValueError(f"No logging config for a specified environment = {environment}")
