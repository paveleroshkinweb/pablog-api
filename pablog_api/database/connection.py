from pablog_api.database.db_manager import MasterSlaveManager
from pablog_api.settings import PostgresSettings

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


PABLOG_SCHEMA = 'pablog'

master_engine: None | AsyncEngine = None
slave_engine: None | AsyncEngine = None
db_manager: None | MasterSlaveManager = None


class PablogBase(AsyncAttrs, DeclarativeBase):
    __table_args__ = {"schema": PABLOG_SCHEMA}

    metadata = MetaData(schema=PABLOG_SCHEMA)


def init_database(db_settings: PostgresSettings, debug: bool = False):
    global master_engine
    global slave_engine
    global db_manager

    # initialize master engine
    master_engine = create_async_engine(
        db_settings.dsn,
        echo=debug,
        future=True,
        pool_size=db_settings.db_connection_pool_size,
        max_overflow=0,
        pool_pre_ping=True,
        isolation_level=db_settings.db_transaction_isolation_level,
        connect_args={'options': f'-csearch_path={PablogBase.metadata.schema}'}
    )

    # initialize slave engine
    slave_engine = None

    db_manager = MasterSlaveManager(master_engine, slave_engine)


async def close_database():
    if not db_manager:
        return

    await db_manager.close()


async def create_database():
    if not db_manager:
        raise RuntimeError("DB Manager has not been initialised!")

    engine = db_manager.get_engine(use_master=True)
    async with engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.create_all)


async def purge_database():
    if not db_manager:
        raise RuntimeError("DB Manager has not been initialised!")

    engine = db_manager.get_engine(use_master=True)
    async with engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.drop_all)


def get_db_manager() -> MasterSlaveManager:
    if not db_manager:
        raise RuntimeError("DB Manager has not been initialised!")
    return db_manager
