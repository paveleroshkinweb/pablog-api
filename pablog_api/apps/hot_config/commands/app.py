import asyncio
import hashlib
import json
import os

from pablog_api.apps.hot_config.constant import CLUSTER_NOTIFICATION_CHANNEL
from pablog_api.apps.hot_config.database import Configuration, get_configuration_repository
from pablog_api.apps.hot_config.schema import ConfigurationBodySchema
from pablog_api.commands.app import app as main_app
from pablog_api.database import close_database, get_db_manager, init_database
from pablog_api.memory_storage import close_redis_cluster, get_redis_cluster, init_redis_cluster
from pablog_api.settings.app import get_app_settings

import structlog


logger = structlog.get_logger(__name__)

settings = get_app_settings()

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "_config", "configuration.json")


async def fetch_config():
    try:
        await init_database(settings.postgres, debug=False)
        db_manager = get_db_manager()
        async with db_manager.master_session() as session:
            config_repository = get_configuration_repository(session)
            latest_config = await config_repository.get_last_config()

            if not latest_config:
                logger.warning("No config found in database! Make sure that configuration is correct")
                return

            logger.info(f"Obtained config, id = {latest_config.id}, checksum = {latest_config.checksum}")
            with open(CONFIG_FILE_PATH, "w") as file:
                config = ConfigurationBodySchema(**latest_config.data)
                file.write(json.dumps(config.model_dump()))
                file.flush()
    finally:
        await close_database()


async def write_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        logger.warning("Couldn't update as the configuration is missing!")
        return

    try:
        await init_database(settings.postgres, debug=False)
        db_manager = get_db_manager()

        async with db_manager.master_session() as session:
            config_repository = get_configuration_repository(session)
            latest_config = await config_repository.get_last_config()

            with open(CONFIG_FILE_PATH) as file:
                config_body_schema = ConfigurationBodySchema(**json.loads(file.read()))
                sha256_hash = hashlib.sha256()
                sha256_hash.update(
                    json.dumps(
                        config_body_schema.model_dump(),
                        sort_keys=True, separators=(',', ':')
                    ).encode()
                )
                checksum = sha256_hash.hexdigest()

                if latest_config and latest_config.checksum == checksum:
                    logger.info("Nothing changed! So do not update cluster settings")
                    return

                logger.info("Writing config to db")

                new_config = Configuration()
                new_config.checksum = checksum
                new_config.data = config_body_schema.model_dump()
                new_config_id = (await config_repository.save_config(new_config)).id
                await session.commit()

        logger.info("Notifying cluster")
        try:
            await init_redis_cluster(settings.cache)
            redis_cluster = get_redis_cluster()
            await redis_cluster.publish(CLUSTER_NOTIFICATION_CHANNEL, new_config_id)
        finally:
            await close_redis_cluster()
    finally:
        await close_database()


@main_app.command(
    name="fetch-config",
    help="Command to fetch last configuration from the database"
)
def fetch_config_command():
    asyncio.run(fetch_config())


@main_app.command(
    name="write-config",
    help="Command to write new config to database and notify cluster"
)
def write_config_command():
    asyncio.run(write_config())
