from abc import ABC, abstractmethod

from pablog_api.apps.auth.database.models import User
from pablog_api.apps.auth.exception import AuthUserAlreadyExistException
from pablog_api.database.connection import get_session
from pablog_api.database.repository import SoftDeleteRepository

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(ABC):

    @abstractmethod
    async def find_by_github_id(self, github_id: int) -> User | None:
        pass

    @abstractmethod
    async def save_user(self, user: User) -> User:
         pass


class RelationalUserRepository(UserRepository, SoftDeleteRepository[User, int]):

    def __init__(self, session: AsyncSession):
        SoftDeleteRepository.__init__(self, User, session)

    async def find_by_github_id(self, github_id: int) -> User | None:
        return await SoftDeleteRepository.select_one(self, [User.github_id == github_id])

    async def save_user(self, user: User) -> User:
        try:
            new_user = await SoftDeleteRepository.save(self, user)
            await self.session.commit()
            return new_user
        except IntegrityError as e:
            raise AuthUserAlreadyExistException from e



async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return RelationalUserRepository(session)
