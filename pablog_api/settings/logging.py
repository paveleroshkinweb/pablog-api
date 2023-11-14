import os

from enum import Enum, unique
from typing import Any

from pablog_api.settings.base import BaseAppSettings
from pablog_api.settings.code_environment import CodeEnvironment

import pydantic
import structlog


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
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.StreamHandler",
                "formatter": "json_formatter",
            },
            "file": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.FileHandler",
                "mode": "a",
                "encoding": "UTF-8",
                "filename": log_file_path,
                "formatter": "json_formatter",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": log_level.value
            }
        }
    }
    return config


def get_test_config() -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {
            "null": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.NullHandler"
            }
        },
        "loggers": {
            "": {
                "level": LoggerLevelType.DEBUG.value,
                "handlers": ["null"]
            }
        }
    }
    return config


def get_prod_config(log_level: LoggerLevelType) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.StreamHandler",
                "formatter": "json_formatter",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level.value
            }
        }
    }
    return config


class LoggingSettings(BaseAppSettings):

    log_level: LoggerLevelType = pydantic.Field(default=LoggerLevelType.INFO)

    log_file_path: str = pydantic.Field(default=os.path.join(os.getcwd(), "logs", "pablog.logs"))

    def get_config(self, environment: CodeEnvironment = CodeEnvironment.DEV) -> dict[str, Any]:
        if environment == CodeEnvironment.DEV:
            return get_dev_config(self.log_level, self.log_file_path)
        elif environment == CodeEnvironment.TEST:
            return get_test_config()
        elif environment == CodeEnvironment.PROD:
            return get_prod_config(self.log_level)
        raise ValueError(f"No logging config for a specified environment = {environment}")
