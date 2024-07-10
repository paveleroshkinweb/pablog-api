# ruff: noqa

import asyncio

from sqlalchemy import select, update, text

from pablog_api.database.models import *
from pablog_api.database.connection import init_database, get_session_factory
from pablog_api.cache.connection import init_cache, get_cache_client
from pablog_api.settings import get_app_settings


settings = get_app_settings()
init_database(settings.postgres, debug=True)

asyncio.run(init_cache(settings.cache, settings.app_name))

session_factory = get_session_factory()
cache_client = get_cache_client()
