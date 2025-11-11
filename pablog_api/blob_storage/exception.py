from pablog_api.exception.base import PablogException


class BlobException(PablogException):
    detail: str = ''


class BlobDeleteException(BlobException):
    pass


class BlobStorageNotSupported(BlobException):
    pass
