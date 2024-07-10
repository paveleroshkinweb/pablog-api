from pablog_api.constant import request_id_ctx_var
from pablog_api.settings import PostgresSettings

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


PABLOG_SCHEMA = 'pablog'

engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None
async_session: None | async_scoped_session = None


class PablogBase(AsyncAttrs, DeclarativeBase):
    __table_args__ = {"schema": PABLOG_SCHEMA}

    metadata = MetaData(schema=PABLOG_SCHEMA)


def bind_session_to_request_id():
    return request_id_ctx_var.get()


def init_database(db_settings: PostgresSettings, debug: bool = False):
    global engine
    global session_factory
    global async_session

    engine = create_async_engine(
        db_settings.dsn,
        echo=debug,
        future=True,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=True,
        connect_args={'options': f'-csearch_path={PablogBase.metadata.schema}'}
    )

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async_session = async_scoped_session(session_factory, scopefunc=bind_session_to_request_id)


async def close_database():
    global engine

    if engine is None:
        return

    await engine.dispose()


async def create_database():
    global engine

    if engine is None:
        return

    async with engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.create_all)


async def purge_database():
    global engine

    if engine is None:
        return

    async with engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.drop_all)
