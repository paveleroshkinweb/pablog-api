import zlib

from enum import IntEnum


class CompressionType(IntEnum):
    NO_COMPRESSION = 0
    BEST_SPEED = 1
    BALANCED = 6
    BEST_COMPRESSION = 9


def zlib_compression(compression_type: CompressionType, data: bytes) -> bytes:
    if compression_type == CompressionType.NO_COMPRESSION:
        return data

    return zlib.compress(data, compression_type)


def zlib_decompression(data: bytes) -> bytes:
    return zlib.decompress(data)
