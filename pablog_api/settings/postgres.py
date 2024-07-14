from pablog_api.constant import IsolationLevel
from pablog_api.settings.base import BaseAppSettings

import pydantic


class PostgresSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "postgres_"

    db_name: str = pydantic.Field()

    db_user: str = pydantic.Field()

    db_password: str = pydantic.Field()

    db_host: str = pydantic.Field(default="127.0.0.1")

    db_port: int = pydantic.Field(default=5432)

    db_scheme: str = "postgresql+psycopg"

    db_transaction_isolation_level: IsolationLevel = pydantic.Field(default=IsolationLevel.READ_COMMITTED)

    db_connection_pool_size: int = pydantic.Field(default=3)

    @property
    def dsn(self) -> str:
        return str(
            pydantic.PostgresDsn.build(
                scheme=self.db_scheme,
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                path=self.db_name
            )
        )
