# ruff: noqa

import asyncio
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import async_scoped_session

from pablog_api.constant import *
from pablog_api.database.models import *
from pablog_api.database import *
from pablog_api.inmemory_storage.connection import init_in_memory_storage
from pablog_api.settings import get_app_settings


settings = get_app_settings()
init_database(settings.postgres, debug=True)

asyncio.run(init_in_memory_storage(settings.cache, settings.app_name))

from pablog_api.database.connection import session_factory, db_manager
from pablog_api.inmemory_storage.connection import init_in_memory_storage
