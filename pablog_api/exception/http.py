from http import HTTPStatus

from pablog_api.exception.base import PablogException

from fastapi.exceptions import HTTPException


class PablogHttpException(PablogException, HTTPException):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    detail: str = HTTPStatus.INTERNAL_SERVER_ERROR.description
    headers: dict[str, str]

    def __init__(self, detail: str = '', headers: None | dict = None):
        PablogException.__init__(self, detail)
        HTTPException.__init__(
            self,
            status_code=self.__class__.status_code,
            detail=(detail or self.__class__.detail),
            headers=(headers or {})
        )


class BadRequestException(PablogHttpException):
    status_code: int = HTTPStatus.BAD_REQUEST
    detail: str = HTTPStatus.BAD_REQUEST.description


class NotFoundException(PablogHttpException):
    status_code: int = HTTPStatus.NOT_FOUND
    detail: str = HTTPStatus.NOT_FOUND.description


class ForbiddenException(PablogHttpException):
    status_code: int = HTTPStatus.FORBIDDEN
    detail: str = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(PablogHttpException):
    status_code: int = HTTPStatus.UNAUTHORIZED
    detail: str = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(PablogHttpException):
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    detail: str = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(PablogHttpException):
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    detail: str = HTTPStatus.UNPROCESSABLE_ENTITY.description
