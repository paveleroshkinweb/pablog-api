from abc import ABC, abstractmethod

from pablog_api.apps.auth.database.models import User
from pablog_api.database.connection import get_session
from pablog_api.database.repository import SoftDeleteRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(ABC):

    @abstractmethod
    async def find_by_github_id(self, github_id: int) -> User | None:
        pass


class SQLUserRepository(UserRepository, SoftDeleteRepository[User, int]):

        def __init__(self, session: AsyncSession):
            SoftDeleteRepository.__init__(self, User, session)

        async def find_by_github_id(self, github_id: int) -> User | None:
            return await super().select_one([User.github_id == github_id])


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return SQLUserRepository(session)
