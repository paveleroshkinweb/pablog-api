# ruff: noqa

import asyncio
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import async_scoped_session

from pablog_api.database.models import *
from pablog_api.database.connection import init_database
from pablog_api.cache.connection import init_cache
from pablog_api.settings import get_app_settings


settings = get_app_settings()
init_database(settings.postgres, debug=True)

asyncio.run(init_cache(settings.cache, settings.app_name))

from pablog_api.database.connection import async_session as session_factory
from pablog_api.cache.connection import cache_client
