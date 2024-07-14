from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from pablog_api.constant import request_id_ctx_var
from pablog_api.settings import PostgresSettings

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


PABLOG_SCHEMA = 'pablog'

engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None
scoped_session_factory: None | async_scoped_session = None


class PablogBase(AsyncAttrs, DeclarativeBase):
    __table_args__ = {"schema": PABLOG_SCHEMA}

    metadata = MetaData(schema=PABLOG_SCHEMA)


def bind_session_to_request_id():
    return request_id_ctx_var.get()


def init_database(db_settings: PostgresSettings, debug: bool = False):
    global engine
    global session_factory
    global scoped_session_factory

    engine = create_async_engine(
        db_settings.dsn,
        echo=debug,
        future=True,
        pool_size=db_settings.db_connection_pool_size,
        max_overflow=0,
        pool_pre_ping=True,
        isolation_level=db_settings.db_transaction_isolation_level,
        connect_args={'options': f'-csearch_path={PablogBase.metadata.schema}'}
    )

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    scoped_session_factory = async_scoped_session(session_factory, scopefunc=bind_session_to_request_id)


async def close_database():
    if not engine:
        return

    await engine.dispose()


async def create_database():
    if not engine:
        raise RuntimeError("Engine has not been initialised!")

    async with engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.create_all)


async def purge_database():
    if not engine:
        raise RuntimeError("Engine has not been initialised!")

    async with engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.drop_all)


@asynccontextmanager
async def get_scoped_session() -> AsyncGenerator[AsyncSession, None]:
    if not scoped_session_factory:
        raise RuntimeError("Session has not been initialised!")

    async with scoped_session_factory() as session:
        yield session


def get_scoped_session_factory() -> async_scoped_session:
    if not scoped_session_factory:
        raise RuntimeError("Session has not been initialised!")
    return scoped_session_factory
