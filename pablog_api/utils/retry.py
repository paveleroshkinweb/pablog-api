import asyncio

from functools import wraps


def async_retry(max_retries=3, base_delay=1, backoff_factor=2, exceptions=(Exception,)):

    def decorator(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                  return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries-1 or not isinstance(e, exceptions):
                        raise
                    await asyncio.sleep(base_delay*(backoff_factor**attempt))

        return inner

    return decorator
