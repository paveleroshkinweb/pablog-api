from enum import Enum, unique


@unique
class CodeEnvironment(str, Enum):
    DEV: str = "DEV"
    PROD: str = "PROD"
