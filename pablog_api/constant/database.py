from enum import IntEnum, StrEnum, auto


class Propagation(IntEnum):

    REQUIRED: int = auto()
    NESTED: int = auto()


class IsolationLevel(StrEnum):

    DEFAULT: str = ""
    READ_UNCOMMITTED: str = "READ UNCOMMITTED"
    READ_COMMITTED: str = "READ COMMITTED"
    REPEATABLE_READ: str = "REPEATABLE READ"
    SERIALIZABLE: str = "SERIALIZABLE"
