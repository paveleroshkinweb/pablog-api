import random

from collections.abc import Sequence
from typing import Any

from pablog_api.exception import PablogException

from sqlalchemy.ext.asyncio import AsyncSession


class MasterSession(AsyncSession):
    pass


class SlaveSession(AsyncSession):

    def _is_clean(self):
        return not self.new and not self.dirty and not self.deleted

    async def flush(self, objects: None | Sequence[Any] = None) -> None:
        # Prevent committing to slave
        if not self._is_clean():
            raise PablogException(detail="Can not commit to slave. Use master instead!")


class MasterSlaveSession:

    def __new__(cls, engines: dict, use_master: bool = True, **kwargs):
        if use_master:
            kwargs['bind'] = engines['master']
            return MasterSession(**kwargs)
        else:
            kwargs['bind'] = random.choice(engines['slaves']) # nosec
            return SlaveSession(**kwargs)
