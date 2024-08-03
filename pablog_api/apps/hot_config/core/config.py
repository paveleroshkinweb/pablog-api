import asyncio
import random

from pablog_api.apps.hot_config.constant import CLUSTER_NOTIFICATION_CHANNEL
from pablog_api.apps.hot_config.database import get_configuration_repository
from pablog_api.apps.hot_config.schema import ConfigurationSchema
from pablog_api.database import get_db_manager
from pablog_api.memory_storage import get_redis_cluster

import structlog


logger = structlog.get_logger(__name__)

# Use random so different workers ping database in different time and don't overwhelm database
_DB_PERIOD_CHECK: int = 120 + random.randint(1, 60)  # nosec

_CONFIG: None | ConfigurationSchema = None

_CONFIG_LOCK: asyncio.Lock = asyncio.Lock()


async def subscribe_to_config_updates():
    asyncio.create_task(subscribe_to_redis_notifications())
    asyncio.create_task(periodic_check_in_db())


async def subscribe_to_redis_notifications():
    global _CONFIG

    logger.info("Subscribing to redis notifications")

    redis_cluster = get_redis_cluster()
    pubsub = redis_cluster.pubsub()
    await pubsub.subscribe(CLUSTER_NOTIFICATION_CHANNEL)

    async for message in pubsub.listen():
        if message['type'] != 'message':
            continue
        new_config_id = int(message['data'])

        logger.info(f"Received notification about new config id = {new_config_id}")

        if _CONFIG and _CONFIG.id >= new_config_id:
            logger.info(f"Skipping update as current version is bigger: {_CONFIG.id} >= {new_config_id}")
            continue

        async with _CONFIG_LOCK:
            try:
                await _update_config_from_db()
            except Exception as e:
                logger.error(f"Unexpected error happened during config update from db: {e}")


async def periodic_check_in_db():
    global _CONFIG

    logger.info("Subscribing to database changes")

    while True:

        await asyncio.sleep(_DB_PERIOD_CHECK)

        async with _CONFIG_LOCK:
            try:
                await _update_config_from_db()
            except Exception as e:
                logger.error(f"Unexpected error happened during config update from db: {e}")


async def _update_config_from_db():
    global _CONFIG

    logger.info("Updating config from database")

    db_manager = get_db_manager()
    async with db_manager.master_session() as session:
        configuration_repository = get_configuration_repository(session)
        db_config = await configuration_repository.get_last_config()

        if _CONFIG.id >= db_config.id:
            logger.info(f"Config was already updated to latest: {_CONFIG.id} >= {db_config.id}")
            return

        new_config_schema = ConfigurationSchema(**{
            'id': db_config.id,
            'data': db_config.data
        })

        _CONFIG.id = new_config_schema.id
        _CONFIG.data = new_config_schema.data

        logger.info(f"New config version = {_CONFIG.id}")


async def set_config_from_db():
    global _CONFIG

    logger.info("Setting initial config from database")

    db_manager = get_db_manager()
    async with db_manager.master_session() as session:
        configuration_repository = get_configuration_repository(session)
        db_config = await configuration_repository.get_last_config()

        _CONFIG = ConfigurationSchema(**{
            'id': db_config.id,
            'data': db_config.data
        })


def get_hot_config():
    return _CONFIG
