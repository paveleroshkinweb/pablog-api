import zlib

from enum import StrEnum


class CompressionType(StrEnum):
    NO_COMPRESSION = "NO_COMPRESSION"
    BEST_SPEED = "BEST_SPEED"
    BALANCED = "BALANCED"
    BEST_COMPRESSION = "BEST_COMPRESSION"


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
