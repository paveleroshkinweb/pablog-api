import logging.config

from pablog_api.settings.app import AppSettings
from pablog_api.settings.code_environment import CodeEnvironment

import structlog


def configure_logger(settings: AppSettings):
    logging.config.dictConfig(settings.logging.get_config(settings.environment))

    # Remove uvicorn loggers
    if settings.environment == CodeEnvironment.DEV:
        uvicorn_error = logging.getLogger("uvicorn.error")
        uvicorn_access = logging.getLogger("uvicorn.access")

        uvicorn_error.disabled = True
        uvicorn_error.propagate = True

        uvicorn_access.disabled = True
        uvicorn_access.propagate = True

    if settings.environment in [CodeEnvironment.DEV, CodeEnvironment.PROD]:
        shared_processors = (
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ExtraAdder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        )
        logger_wrapper = structlog.stdlib.BoundLogger
        structlog.configure(
            processors=shared_processors,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=logger_wrapper,
            cache_logger_on_first_use=True,
        )
