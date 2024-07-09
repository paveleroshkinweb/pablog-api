import structlog

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


ACCESS_LOGS_BLACKLIST = ["/api/v1/healthcheck"]


class LogRequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        logger = structlog.get_logger(__name__)

        structlog.contextvars.clear_contextvars()

        request_id = request.headers.get("X-Request-Id", "")

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
        )

        # Do not log utils requests
        should_log_request = not any(request.url.path.startswith(pattern) for pattern in ACCESS_LOGS_BLACKLIST)
        if should_log_request:
            logger.info("Received new request")
            response = await call_next(request)
            logger.info("Processed request")
        else:
            response = await call_next(request)

        return response
