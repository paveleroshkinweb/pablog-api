import logging
import logging.config
import sys

from pablog_api.settings.app import AppSettings


def configure_logger(settings: AppSettings):
    config = settings.logging.get_config(settings.environment)

    if not config:
        return

    logging.config.dictConfig(config)

    logger = logging.getLogger()

    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        Log any uncaught exception instead of letting it be printed by Python
        (but leave KeyboardInterrupt untouched to allow users to Ctrl+C to stop)
        See https://stackoverflow.com/a/16993115/3641865
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception
