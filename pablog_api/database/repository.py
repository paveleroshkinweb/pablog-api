from typing import Generic, TypeVar

from pablog_api.database.models.models import PablogBase, PrimaryKeyType, SoftDeleteModelType

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType", bound=PablogBase)


class BaseRelationalRepository(Generic[ModelType, PrimaryKeyType]):

    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: PrimaryKeyType) -> ModelType | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def save(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType):
        await self.delete_by_id(instance.id)

    async def delete_by_id(self, id: PrimaryKeyType):
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)


SoftDeleteType = TypeVar("SoftDeleteType", bound=SoftDeleteModelType)


class SoftDeleteRepository(BaseRelationalRepository[SoftDeleteType, PrimaryKeyType]):

    async def delete(self, instance: SoftDeleteType):
        instance.is_deleted = True
        await self.save(instance)

    async def delete_by_id(self, id: PrimaryKeyType):
        stmt = update(self.model).where(self.model.id == id).values(is_deleted=True)
        await self.session.execute(stmt)
