from enum import Enum, unique


@unique
class CodeEnvironment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"
    CI = "CI"
