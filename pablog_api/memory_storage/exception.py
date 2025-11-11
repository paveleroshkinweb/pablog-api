from pablog_api.exception.base import PablogException


class MemoryStorageException(PablogException):
    detail: str = ''


class MemoryStorageNotSupportedException(MemoryStorageException):
    pass
