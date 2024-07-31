import time

from contextlib import asynccontextmanager, contextmanager

import structlog


logger = structlog.get_logger(__name__)


@contextmanager
def sync_stats(metric_subtype: str):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        time_took = end_time - start_time
        logger.info(metric_type="stats", metric_subtype=metric_subtype, time=time_took)


@asynccontextmanager
def async_stats(metric_subtype: str):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        time_took = end_time - start_time
        logger.info(metric_type="stats", metric_subtype=metric_subtype, time=time_took)
