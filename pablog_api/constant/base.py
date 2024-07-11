from contextvars import ContextVar
from enum import StrEnum


REQUEST_ID_HEADER: str = "X-Request-Id"

request_id_ctx_var: ContextVar[None | str] = ContextVar(REQUEST_ID_HEADER, default=None)


class IsolationLevel(StrEnum):
    READ_UNCOMMITTED: str = "READ UNCOMMITTED"
    READ_COMMITTED: str = "READ COMMITTED"
    REPEATABLE_READ: str = "REPEATABLE READ"
    SERIALIZABLE: str = "SERIALIZABLE"
