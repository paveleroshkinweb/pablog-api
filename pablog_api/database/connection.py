from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


PABLOG_SCHEMA = 'pablog'


engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None


class PablogBase(AsyncAttrs, DeclarativeBase):
    pass


def init_database(dsn: str, debug: bool = False):
    global engine
    global session_factory

    engine = create_async_engine(
        dsn,
        echo=debug,
        future=True,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=True,
        connect_args={'options': f'-csearch_path={PABLOG_SCHEMA}'}
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
