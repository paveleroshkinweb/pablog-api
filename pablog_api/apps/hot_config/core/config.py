from asyncio import Lock

from pablog_api.apps.hot_config.constant import CLUSTER_NOTIFICATION_CHANNEL
from pablog_api.apps.hot_config.database import get_configuration_repository
from pablog_api.apps.hot_config.schema import ConfigurationSchema
from pablog_api.database import get_db_manager
from pablog_api.memory_storage import get_redis_cluster

import structlog


logger = structlog.get_logger(__name__)

CONFIG = None
_CONFIG_LOCK = Lock()


async def subscribe_to_config_updates():
    global CONFIG

    redis_cluster = get_redis_cluster()
    pubsub = redis_cluster.pubsub()
    await pubsub.subscribe(CLUSTER_NOTIFICATION_CHANNEL)

    async for message in pubsub.listen():
        if message['type'] != 'message':
            continue
        new_config_id = int(message['data'])

        logger.info(f"Received notification about new config id = {new_config_id}")

        if CONFIG and CONFIG.id >= new_config_id:
            logger.info(f"Skipping update as current version is bigger: {CONFIG.id} >= {new_config_id}")
            continue

        async with _CONFIG_LOCK:
            logger.info("Updating config from database")
            db_manager = get_db_manager()
            try:
                async with db_manager.master_session() as session:
                    configuration_repository = get_configuration_repository(session)
                    db_config = await configuration_repository.get_last_config()
                    if not db_config:
                        logger.error("Config was deleted from db?")
                        continue
                    if CONFIG.id >= db_config.id:
                        logger.info(f"Config was already updated to latest: {CONFIG.id} >= {db_config.id}")
                    else:
                        new_config_schema = ConfigurationSchema(**{
                            'id': db_config.id,
                            'data': db_config.data
                        })

                        CONFIG.id = new_config_schema.id
                        CONFIG.data = new_config_schema.data

                        logger.info(f"New config version = {CONFIG.id}")
            except Exception as e:
                logger.error(f"Unexpected error happened during config update from db: {e}")


async def set_config_from_db():
    global CONFIG

    logger.info("Setting initial config from database")

    db_manager = get_db_manager()
    async with db_manager.master_session() as session:
        configuration_repository = get_configuration_repository(session)
        db_config = await configuration_repository.get_last_config()

        CONFIG = ConfigurationSchema(**{
            'id': db_config.id,
            'data': db_config.data
        })


def get_hot_config():
    return CONFIG
