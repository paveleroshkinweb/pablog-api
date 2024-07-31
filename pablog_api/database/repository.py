from typing import Generic, TypeVar

from pablog_api.database.models.models import PablogBase, PrimaryKeyType, SoftDeleteModelType

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType", bound=PablogBase)


class BaseRelationalRepository(Generic[ModelType, PrimaryKeyType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, id: PrimaryKeyType) -> ModelType | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )
        result = await session.execute(stmt)
        return result.scalar()

    async def save(self, session: AsyncSession, instance: ModelType) -> ModelType:
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def delete(self, session: AsyncSession, instance: ModelType):
        await self.delete_by_id(session, instance.id)

    async def delete_by_id(self, session: AsyncSession, id: PrimaryKeyType):
        stmt = delete(self.model).where(self.model.id == id)
        await session.execute(stmt)


SoftDeleteType = TypeVar("SoftDeleteType", bound=SoftDeleteModelType)


class SoftDeleteRepository(BaseRelationalRepository[SoftDeleteType, PrimaryKeyType]):

    async def delete(self, session: AsyncSession, instance: SoftDeleteType):
        instance.is_deleted = True
        await self.save(session, instance)

    async def delete_by_id(self, session: AsyncSession, id: PrimaryKeyType):
        stmt = update(self.model).where(self.model.id == id).values(is_deleted=True)
        await session.execute(stmt)
