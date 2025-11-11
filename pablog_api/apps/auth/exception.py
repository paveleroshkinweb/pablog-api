from pablog_api.exception.base import PablogException


class AuthException(PablogException):
    detail: str = ''


class AuthUserAlreadyExistException(AuthException):
    pass
