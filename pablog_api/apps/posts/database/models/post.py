from datetime import datetime

from pablog_api.database.models import IntPrimaryKeyMixin

from sqlalchemy import JSON, Integer, LargeBinary, String, text
from sqlalchemy.orm import Mapped, mapped_column


class Post(IntPrimaryKeyMixin):

    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    body: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False
    )

    mins_to_read: Mapped[int] = mapped_column(
        Integer,
        server_default=text("0"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    tags: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=True
    )
