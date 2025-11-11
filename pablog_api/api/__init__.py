import logging
import sys

from contextlib import asynccontextmanager
from http import HTTPStatus

from pablog_api.api.v1 import router as v1_router
from pablog_api.constant import REQUEST_ID_HEADER, request_id_ctx_var
from pablog_api.database.connection import close_database, init_database
from pablog_api.exception import PablogException, PablogHttpException
from pablog_api.memory_storage import close_redis_cluster, init_redis_cluster
from pablog_api.middleware import AddRequestIDMiddleware
from pablog_api.schema.error import ErrorResponse
from pablog_api.settings.app import get_app_settings

import structlog

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import ORJSONResponse


settings = get_app_settings()

logging.config.dictConfig(settings.logging.get_config(settings.environment))
structlog.configure_once(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True
)

logger = structlog.get_logger("pablog_api.unhandled")

def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """
    Log any uncaught exception instead of letting it be printed by Python
    (but leave KeyboardInterrupt untouched to allow users to Ctrl+C to stop)
    See https://stackoverflow.com/a/16993115/3641865
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.exception(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )

sys.excepthook = handle_uncaught_exception


logger = structlog.get_logger(__name__)

DOCS_URL = "/docs/openapi" if settings.is_development else None
OPENAPI_URL = "/docs/openapi.json" if settings.is_development else None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing infrastructure connections")

    await init_database(settings.sqlite)
    await init_redis_cluster(settings.cache)

    yield
    await close_redis_cluster()
    await close_database()


async def handle_exception(request: Request, exception: Exception):
    request_data = {
        'url': str(request.url),
        'method': request.method,
        'query_string': dict(request.query_params),
    }

    logger.exception(exception, **request_data)

    headers = {REQUEST_ID_HEADER: request_id_ctx_var.get()}

    if isinstance(exception, PablogHttpException):
        error_response = ErrorResponse(message=exception.detail)
        return ORJSONResponse(
            status_code=exception.status_code,
            content=error_response.model_dump(),
            headers={**headers, **exception.headers}
        )
    elif isinstance(exception, PablogException):
        error_response = ErrorResponse(message=exception.detail)
        return ORJSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
            headers=headers
        )
    else:
        error_response = ErrorResponse(message=HTTPStatus.INTERNAL_SERVER_ERROR.description)
        return ORJSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
            headers=headers
        )


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    docs_url=DOCS_URL,
    openapi_url=OPENAPI_URL,
    default_response_class=ORJSONResponse,
    version=settings.app_version,
    contact={
        "name": "Pavel Yaroshkin",
        "url": "https://github.com/paveleroshkinweb/pablog-api",
        "email": "eroshkin321@gmail.com"
    }
)

app.add_exception_handler(Exception, handle_exception)
app.add_middleware(AddRequestIDMiddleware, environment=settings.environment)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)

app.include_router(api_router)
