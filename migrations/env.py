import os

from logging.config import fileConfig

from pablog_api.apps.hot_config.database.models import *  # type: ignore # noqa: F403
from pablog_api.database.models import *  # type: ignore # noqa: F403

from alembic import context
from sqlalchemy import engine_from_config, pool


DB_USER = os.environ.get("postgres_db_user", "pablog")
DB_PASSWORD = os.environ.get("postgres_db_password", "pablog")
DB_HOST = os.environ.get("postgres_db_host", "127.0.0.1")
DB_PORT = os.environ.get('postgres_db_port', "5432")
DB_NAME = os.environ.get("postgres_db_name", "pablog")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "postgres_db_user", DB_USER)
config.set_section_option(section, "postgres_db_password", DB_PASSWORD)
config.set_section_option(section, "postgres_db_host", DB_HOST)
config.set_section_option(section, "postgres_db_port", DB_PORT)
config.set_section_option(section, "postgres_db_name", DB_NAME)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = PablogBase.metadata  # type: ignore # noqa: F405

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        version_table_schema=target_metadata.schema,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True
        )

        with context.begin_transaction():
            context.execute(f'create schema if not exists {target_metadata.schema};')
            context.execute(f'set search_path to {target_metadata.schema},public')
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
