import logging
import logging.config
import sys

from pablog_api.settings.app import AppSettings

import structlog


def configure_logger(settings: AppSettings):
    config = settings.logging.get_config(settings.environment)

    if not config:
        return

    logging.config.dictConfig(config)

    structlog.configure_once(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )

    logger = structlog.get_logger("pablog_api.unhandled")

    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        Log any uncaught exception instead of letting it be printed by Python
        (but leave KeyboardInterrupt untouched to allow users to Ctrl+C to stop)
        See https://stackoverflow.com/a/16993115/3641865
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.exception(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception
