from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager

from pablog_api.database import close_database, create_database, init_database, purge_database
from pablog_api.logging_utils.setup_logger import configure_logger
from pablog_api.settings.app import get_app_settings

import structlog

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse, Response


settings = get_app_settings()

configure_logger(settings)

API_VERSION = "v1"

API_PATH_V1 = f"/api/{API_VERSION}"

VERSION = "0.1.0"

ACCESS_LOGS_BLACKLIST = ["/healthcheck", "/docs"]


logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database(dsn=settings.postgres.dsn, debug=settings.is_development())

    # Just a temporal hack for test purposes before migrations are integrated
    await purge_database()
    await create_database()

    yield
    await close_database()


app = FastAPI(
    lifespan=lifespan,
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

    # Do not log utils requests
    shouldLogRequest = not any(request.url.path.startswith(pattern) for pattern in ACCESS_LOGS_BLACKLIST)
    if shouldLogRequest:
        logger.info("Received new request")
        response = await call_next(request)
        logger.info("Processed request")
    else:
        response = await call_next(request)

    return response


@app.get("/healthcheck")
def healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@app.get(f"{API_PATH_V1}/info")
def info() -> Response:
    return ORJSONResponse(status_code=status.HTTP_200_OK, content={"version": VERSION})
