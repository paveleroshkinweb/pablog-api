import uuid

from collections.abc import AsyncGenerator

from pablog_api.constant import request_id_ctx_var
from pablog_api.settings import SQLiteSettings
from pablog_api.utils import async_retry

from sqlalchemy import event, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None
scoped_session: None | async_scoped_session = None


def bind_session_to_request_id():
    request_id = request_id_ctx_var.get()
    return request_id or str(uuid.uuid4())


async def init_database(db_settings: SQLiteSettings):
    global engine
    global session_factory
    global scoped_session

    engine = create_async_engine(
        db_settings.dsn,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )

    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    scoped_session = async_scoped_session(session_factory, scopefunc=bind_session_to_request_id)

    def set_pragmas(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute(f"PRAGMA busy_timeout={db_settings.busy_timeout};")
        cursor.close()

    event.listen(engine.sync_engine, "connect", set_pragmas)

    await ping()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if not scoped_session:
        raise RuntimeError

    async with scoped_session() as session:
        yield session


@async_retry(max_retries=5, backoff_factor=2, exceptions=(OperationalError,))
async def ping():
    if not scoped_session:
        raise RuntimeError

    async with scoped_session() as session:
        await session.execute(text("SELECT 1;"))


async def close_database():
    if not engine:
        return

    try:
        await engine.dispose()
    except Exception:
        pass
