from enum import IntEnum, StrEnum, auto


class Propagation(IntEnum):

    REQUIRED = auto()
    NESTED = auto()


class IsolationLevel(StrEnum):

    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"
