import uuid

from pablog_api.constant import REQUEST_ID_HEADER, request_id_ctx_var
from pablog_api.exception import BadRequestException
from pablog_api.settings import CodeEnvironment

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
from structlog.contextvars import bind_contextvars


class AddRequestIDMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, environment: CodeEnvironment):
        super().__init__(app)
        self.environment = environment

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER, "")

        if self.environment == CodeEnvironment.PROD and not request_id:
            raise BadRequestException(detail=f"{REQUEST_ID_HEADER} header is required!")

        # Generate random request_id just for development purposes
        if not request_id:
            request_id = str(uuid.uuid4())

        request_id_ctx_var.set(request_id)
        bind_contextvars(request_id=request_id)

        response = await call_next(request)

        response.headers[REQUEST_ID_HEADER] = request_id
        return response
