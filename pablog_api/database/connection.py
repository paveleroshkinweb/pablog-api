from pablog_api.database.db_manager import MasterSlaveManager
from pablog_api.database.models import PablogBase
from pablog_api.database.session import MasterSlaveSession
from pablog_api.settings import PostgresSettings

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


master_engine: None | AsyncEngine = None
slave_engine: None | AsyncEngine = None
session_factory: None | async_sessionmaker = None
db_manager: None | MasterSlaveManager = None


def init_database(db_settings: PostgresSettings, debug: bool = False):
    global master_engine
    global slave_engine
    global session_factory
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

    engines = {
        'master': master_engine,
        # Currently use master as slave before replication is implemented
        'slaves': [master_engine]
    }

    session_factory = async_sessionmaker(class_=MasterSlaveSession, engines=engines, autoflush=True)

    db_manager = MasterSlaveManager(session_factory=session_factory)


async def close_database():
    if not db_manager:
        return

    await db_manager.close()


async def create_database():
    if not master_engine:
        raise RuntimeError("Master engine has not been initialised!")

    async with master_engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.create_all)


async def purge_database():
    if not master_engine:
        raise RuntimeError("Master engine has not been initialised!")

    async with master_engine.begin() as connection:
        await connection.run_sync(PablogBase.metadata.drop_all)


def get_db_manager() -> MasterSlaveManager:
    if not db_manager:
        raise RuntimeError("DB Manager has not been initialised!")
    return db_manager
