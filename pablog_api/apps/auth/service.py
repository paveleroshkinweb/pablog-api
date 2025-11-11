from pablog_api.apps.auth.database.models import User
from pablog_api.apps.auth.database.repository import UserRepository, get_user_repository

from fastapi import Depends


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def find_by_github_id(self, github_id: int) -> User | None:
        return await self.repository.find_by_github_id(github_id)


async def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)
