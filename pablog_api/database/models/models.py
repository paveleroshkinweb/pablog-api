import uuid

from datetime import datetime
from typing import Generic, TypeVar

from sqlalchemy import MetaData, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


PABLOG_SCHEMA = 'pablog'

PrimaryKeyType = TypeVar("PrimaryKeyType", int, str, uuid.UUID)


class PablogBase(AsyncAttrs, DeclarativeBase, Generic[PrimaryKeyType]):
    __abstract__ = True

    __table_args__ = {"schema": PABLOG_SCHEMA}

    metadata = MetaData(schema=PABLOG_SCHEMA)

    id: Mapped[PrimaryKeyType] = mapped_column(primary_key=True)


class UUIDPrimaryKeyMixin(PablogBase[uuid.UUID]):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )


class IntPrimaryKeyMixin(PablogBase[int]):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class StringPrimaryKeyMixin(PablogBase[str]):
    __abstract__ = True

    id: Mapped[str] = mapped_column(primary_key=True)


class TimestampMixin:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=text("current_timestamp(0)")
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        server_default=text("current_timestamp(0)")
    )


class SoftDeleteMixin:
    __abstract__ = True

    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    is_deleted: Mapped[bool] = mapped_column(default=False)


class SoftDeleteModelType(PablogBase[PrimaryKeyType], SoftDeleteMixin):
    __abstract__ = True
