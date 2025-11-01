from .base import PablogException


class BlobException(PablogException):
    detail: str = ''


class DeleteBlobException(BlobException):
    pass
