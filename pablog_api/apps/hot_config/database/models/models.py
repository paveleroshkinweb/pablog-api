from datetime import datetime

from pablog_api.database.models import IntPrimaryKeyMixin, PablogBase

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Configuration(IntPrimaryKeyMixin, PablogBase[int]):
    __tablename__ = "config"

    checksum: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=text("current_timestamp(0)"),
    )

    data: Mapped[dict] = mapped_column(JSON, nullable=False)
