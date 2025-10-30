import logging

from collections.abc import AsyncGenerator

from pablog_api.settings import LoggerLevelType, SQLiteSettings
from pablog_api.utils import async_retry

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None


async def init_database(db_settings: SQLiteSettings, debug: bool = False):
    global engine
    global session_factory

    engine = create_async_engine(
        db_settings.dsn,
        echo=False,
        future=True,
    )

    # Hack to overwrite default echo=True handler
    if debug:
        logging.getLogger("sqlalchemy.engine").setLevel(LoggerLevelType.DEBUG)

    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=True)
    await ping()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if not session_factory:
        raise RuntimeError

    async with session_factory() as session:
        yield session


@async_retry(max_retries=5, exceptions=(OperationalError,))
async def ping():
    if not session_factory:
        raise RuntimeError

    async with session_factory() as session:
        await session.execute(text("SELECT 1;"))


async def close_database():
    if not engine:
        return

    try:
        await engine.dispose()
    except Exception:
        pass

# def bind_session_to_request_id():
#     request_id = request_id_ctx_var.get()
#     # In shell environment
#     if not request_id:
#         request_id = uuid.uuid4()
#     return request_id
