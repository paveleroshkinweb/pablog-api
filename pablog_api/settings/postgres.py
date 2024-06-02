from pablog_api.settings.base import BaseAppSettings

import pydantic


class PostgresSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "postgres_"

    db_name: str = pydantic.Field()

    db_user: str = pydantic.Field()

    db_password: str = pydantic.Field()

    db_host: str = pydantic.Field(default="localhost")

    db_port: int = pydantic.Field(default=5432)

    db_scheme: str = "postgresql+psycopg"

    @property
    def dsn(self) -> str:
        return str(
            pydantic.PostgresDsn.build(
                scheme=self.db_scheme,
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                path=f"/{self.db_name}",
            )
        )
