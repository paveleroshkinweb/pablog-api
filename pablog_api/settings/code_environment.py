from enum import Enum, unique


@unique
class CodeEnvironment(str, Enum):
    CI= "CI"
    DEV = "DEV"
    PROD = "PROD"
