from collections.abc import Awaitable, Callable

from pablog_api.logging_utils.setup_logger import configure_logger
from pablog_api.settings.app import get_app_settings

import structlog

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse, Response


settings = get_app_settings()

configure_logger(settings)

API_VERSION = "v1"

API_PATH_V1 = f"/api/{API_VERSION}"

VERSION = "1.0.0"

ACCESS_LOGS_BLACKLIST = [f"{API_PATH_V1}/status"]

app = FastAPI(
    title="PablogAPI",
    docs_url="/docs/openapi",
    openapi_url="/docs/openapi.json",
    default_response_class=ORJSONResponse,
    version=VERSION,
)


@app.middleware("http")
async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    structlog.contextvars.clear_contextvars()

    request_id = request.headers.get("X-Request-Id", "")

    structlog.contextvars.bind_contextvars(
        request_id=request_id,
    )

    response = await call_next(request)

    return response


@app.get("/api/healthcheck")
def healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@app.get("/api/info")
def info() -> Response:
    return ORJSONResponse(status_code=status.HTTP_200_OK, content={"version": VERSION})


def run_dev_server():
    import uvicorn
    uvicorn.run(
        "pablog_api.api.server:app",
        host=settings.service_settings.api_host,
        port=settings.service_settings.api_port,
        log_config=settings.logging.get_config(settings.environment),
        reload=settings.is_development()
    )
