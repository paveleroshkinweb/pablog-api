from pablog_api.settings import PostgresSettings

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


PABLOG_SCHEMA = 'pablog'


engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None


class PablogBase(AsyncAttrs, DeclarativeBase):
    __table_args__ = {"schema": PABLOG_SCHEMA}

    metadata = MetaData(schema=PABLOG_SCHEMA)


def init_database(db_settings: PostgresSettings, debug: bool = False):
    global engine
    global session_factory

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


def get_session_factory() -> None | async_sessionmaker:
    return session_factory
