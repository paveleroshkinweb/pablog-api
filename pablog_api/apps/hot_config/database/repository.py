from abc import ABC, abstractmethod
from functools import lru_cache

from pablog_api.apps.hot_config.database.models import Configuration
from pablog_api.database.repository import BaseRelationalRepository

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class IConfigurationRepository(ABC):

    @abstractmethod
    async def get_last_config(self) -> None | Configuration:
        pass

    @abstractmethod
    async def save_config(self, data: Configuration):
        pass


class ConfigurationRepository(BaseRelationalRepository[Configuration, int], IConfigurationRepository):

    def __init__(self, session: AsyncSession):
        BaseRelationalRepository.__init__(self, Configuration, session)

    async def get_last_config(self) -> None | Configuration:
        find_max_config_id = select(func.max(self.model.id))
        result = await self.session.scalar(select(Configuration).filter(Configuration.id == find_max_config_id))
        return result

    async def save_config(self, data: Configuration):
        await self.save(data)


@lru_cache(maxsize=1)
def get_configuration_repository(session: AsyncSession) -> IConfigurationRepository:
    return ConfigurationRepository(session)
