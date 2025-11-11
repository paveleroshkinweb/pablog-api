import time

from contextlib import asynccontextmanager, contextmanager

import structlog


logger = structlog.get_logger(__name__)


# TODO: refactor this shitty module

@contextmanager
def sync_stats(metric_subtype: str):
    from pablog_api.settings import get_app_settings

    if not get_app_settings().enable_stats:
        yield
    else:
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            time_took = end_time - start_time
            logger.info(metric_type="stats", metric_subtype=metric_subtype, time=time_took)


@asynccontextmanager
async def async_stats(metric_subtype: str):
    from pablog_api.settings import get_app_settings

    if not get_app_settings().enable_stats:
        yield
    else:
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            time_took = end_time - start_time
            logger.info(metric_type="stats", metric_subtype=metric_subtype, time=time_took)
