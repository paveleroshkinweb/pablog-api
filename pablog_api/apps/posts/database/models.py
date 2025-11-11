from pablog_api.database.models import IntPrimaryKeyMixin, SoftDeleteMixin, TimestampMixin

from sqlalchemy import JSON, Integer, LargeBinary, String, text
from sqlalchemy.orm import Mapped, mapped_column


class Post(IntPrimaryKeyMixin, SoftDeleteMixin, TimestampMixin):

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

    tags: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list
    )
