import logging

from collections.abc import Awaitable, Callable

from pablog_api.settings.app import settings
from pablog_api.utils.setup_logger import configure_logger

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse, Response


configure_logger(settings)

API_VERSION = "v1"

API_PATH_V1 = f"/api/{API_VERSION}"

VERSION = "1.0.0"


app = FastAPI(
    title="PablogAPI",
    docs_url="/docs/openapi",
    openapi_url="/docs/openapi.json",
    default_response_class=ORJSONResponse,
    version=VERSION,
)


@app.middleware("http")
async def trace_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    logger = logging.getLogger(__name__)
    request_id = request.headers.get('X-Request-Id')

    if not request_id:
        logger.warning("No X-Request-Id was provided!")

    response: Response = await call_next(request)

    return response


@app.get(f"{API_PATH_V1}/ping", status_code=status.HTTP_200_OK)
def pong() -> Response:
    return Response(status_code=status.HTTP_200_OK)


def run_dev_server():
    import uvicorn
    uvicorn.run(
        "pablog_api.api.server:app",
        host=settings.service_settings.api_host,
        port=settings.service_settings.api_port,
        log_config=settings.logging.get_config(settings.environment),
        reload=settings.is_development()
    )
