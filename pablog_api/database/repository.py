from functools import cached_property
from typing import Generic, TypeVar

from pablog_api.database.models import PablogBase, PrimaryKeyType, SoftDeleteModelType

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement


ModelType = TypeVar("ModelType", bound=PablogBase)


class BaseRelationalRepository(Generic[ModelType, PrimaryKeyType]):

    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def select(self, filters: list[ColumnElement], order_by: ColumnElement | None = None, limit: int | None = None,
                     offset: int | None = None) -> list[ModelType]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.where(*filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def select_one(self, filters: list[ColumnElement]) -> ModelType | None:
        assert filters
        stmt = select(self.model).where(*filters)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, id: PrimaryKeyType) -> ModelType | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def save(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.delete_by_id(instance.id)

    async def delete_by_id(self, id: PrimaryKeyType) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.flush()


SoftDeleteType = TypeVar("SoftDeleteType", bound=SoftDeleteModelType)


class SoftDeleteRepository(BaseRelationalRepository[SoftDeleteType, PrimaryKeyType]):

    @cached_property
    def __is_not_deleted_filter(self):
        return self.model.is_deleted.is_(False)

    def __prepare_filters(self, filters):
        if not filters:
            filters = [self.__is_not_deleted_filter]
        else:
            filters.append(self.__is_not_deleted_filter)
        return filters

    async def select_active(self, filters: list[ColumnElement], order_by: ColumnElement | None = None, limit: int | None = None,
                     offset: int | None = None) -> list[SoftDeleteType]:
        return await super().select(self.__prepare_filters(filters), order_by=order_by, limit=limit, offset=offset)

    async def select_one_active(self, filters: list[ColumnElement]) -> SoftDeleteType | None:
        return await super().select_one(self.__prepare_filters(filters))

    async def delete_by_id(self, id: PrimaryKeyType) -> None:
        stmt = update(self.model).where(self.model.id == id).values(is_deleted=True)
        await self.session.execute(stmt)
        await self.session.flush()
