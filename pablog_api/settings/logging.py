import logging
import os
import time

from enum import StrEnum
from typing import Any

from pablog_api.settings.base import BaseAppSettings
from pablog_api.settings.code_environment import CodeEnvironment

import pydantic
import structlog


logging.Formatter.converter = time.gmtime


class LoggerLevelType(StrEnum):
    CRITICAL: str = "CRITICAL"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"
    INFO: str = "INFO"
    DEBUG: str = "DEBUG"


def get_ci_config(log_level: LoggerLevelType) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json_formatter",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level
            },
            "sqlalchemy.engine": {
                "level": LoggerLevelType.WARNING,
                "handlers": ["console"],
                "propagate": False,
                "qualname": "sqlalchemy.engine"
            },
            "gunicorn.error": {
                "level": LoggerLevelType.CRITICAL,
                "handlers": ["console"],
                "propagate": False,
                "qualname": "gunicorn.error"
            },
        }
    }
    return config


def get_dev_config(log_level: LoggerLevelType, log_file_path: str) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json_formatter"
            },
            "file": {
                "level": LoggerLevelType.DEBUG,
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
                "level": log_level
            },
            "gunicorn.error": {
                "level": LoggerLevelType.INFO,
                "handlers": ["console", "file"],
                "propagate": False,
                "qualname": "gunicorn.error"
            },
        }
    }
    return config


def get_prod_config(log_level: LoggerLevelType) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json_formatter",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level
            },
            "sqlalchemy.engine": {
                "level": LoggerLevelType.WARNING,
                "handlers": ["console"],
                "propagate": False,
                "qualname": "sqlalchemy.engine"
            },
            "gunicorn.error": {
                "level": LoggerLevelType.CRITICAL,
                "handlers": ["console"],
                "propagate": False,
                "qualname": "gunicorn.error"
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
        elif environment == CodeEnvironment.PROD:
            return get_prod_config(self.log_level)
        elif environment == CodeEnvironment.CI:
            return get_ci_config(self.log_level)
        else:
            return {}
