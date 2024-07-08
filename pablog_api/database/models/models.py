import uuid

from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class UUIDMixin:

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )


class TimestampMixin:

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

    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    is_deleted: Mapped[bool] = mapped_column(default=False)
