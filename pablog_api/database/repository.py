from typing import Generic, TypeVar

from pablog_api.database.models.models import PablogBase, PrimaryKeyType

from sqlalchemy import delete, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType", bound=PablogBase)


class BaseRepository(Generic[ModelType, PrimaryKeyType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, id: PrimaryKeyType) -> ModelType | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )
        result = await session.execute(stmt)
        return result.scalar()

    async def save(self, session: AsyncSession, data: ModelType) -> ModelType:
        inspr = inspect(data)
        if not inspr.modified and inspr.has_identity:
            return data

        session.add(data)
        await session.flush()
        await session.refresh(data)
        return data

    async def delete(self, session: AsyncSession, id: PrimaryKeyType):
        stmt = delete(self.model).where(self.model.id == id)
        await session.execute(stmt)
