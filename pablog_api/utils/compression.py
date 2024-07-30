import zlib

from enum import StrEnum


class CompressionType(StrEnum):
    NO_COMPRESSION: str = "NO_COMPRESSION"
    BEST_SPEED: str = "BEST_SPEED"
    BALANCED: str = "BALANCED"
    BEST_COMPRESSION: str = "BEST_COMPRESSION"


COMPRESSION_LEVEL_MAP = {
    CompressionType.NO_COMPRESSION: 0,
    CompressionType.BEST_SPEED: 1,
    CompressionType.BALANCED: 6,
    CompressionType.BEST_COMPRESSION: 9
}


def zlib_compression(compression_type: CompressionType, data: bytes) -> bytes:
    if type == CompressionType.NO_COMPRESSION:
        return data

    level = COMPRESSION_LEVEL_MAP[compression_type]
    return zlib.compress(data, level)


def zlib_decompression(data: bytes) -> bytes:
    return zlib.decompress(data)
