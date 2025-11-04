from datetime import datetime

from pablog_api.database.models import IntPrimaryKeyMixin

from sqlalchemy import JSON, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column


class User(IntPrimaryKeyMixin):

    __tablename__ = "users"

    github_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True
    )

    username: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    roles: Mapped[list[int]] = mapped_column(
        JSON,
        nullable=False,
        default=list
    )
