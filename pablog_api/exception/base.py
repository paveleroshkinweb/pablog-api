from http import HTTPStatus


class PablogException(Exception):
    http_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequestException(PablogException):
    http_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(PablogException):
    http_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(PablogException):
    http_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(PablogException):
    http_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(PablogException):
    http_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(PablogException):
    http_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description
