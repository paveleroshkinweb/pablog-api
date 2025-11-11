from pablog_api.apps.auth.database.models import User
from pablog_api.apps.auth.database.repository import UserRepository, get_user_repository

import structlog

from fastapi import Depends


logger = structlog.get_logger(__name__)
metric_type = "auth"

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def find_by_github_id(self, github_id: int) -> User | None:
        return await self.repository.find_by_github_id(github_id)

    async def save_user(self, user: User) -> User:
        new_user = await self.repository.save_user(user)
        log_data = {
            'id': new_user.id,
            'username': new_user.username
        }
        logger.info(metric_type=metric_type, metric_subtype="created_user", data=log_data)
        return new_user


async def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)
