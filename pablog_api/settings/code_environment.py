from enum import Enum, unique


@unique
class CodeEnvironment(str, Enum):
    DEV: str = "DEV"
    TEST: str = "TEST"
    PROD: str = "PROD"
