from pablog_api.constant import REQUEST_ID_HEADER
from pablog_api.schema.response import ErrorResponse
from pablog_api.settings import CodeEnvironment

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class RequiredRequestID(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, environment: CodeEnvironment):
        super().__init__(app)
        self.environment = environment

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER, "")

        if self.environment == CodeEnvironment.PROD and not request_id:
            error_response = ErrorResponse(
                request_id=request_id,
                message=f"{REQUEST_ID_HEADER} header is required!"
            )

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response.model_dump()
            )

        return await call_next(request)
