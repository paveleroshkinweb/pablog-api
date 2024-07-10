from contextlib import asynccontextmanager

from pablog_api.api.v1 import router as v1_router
from pablog_api.cache import init_cache
from pablog_api.database import close_database, init_database
from pablog_api.logging_utils.setup_logger import configure_logger
from pablog_api.middleware import AddRequestIDMiddleware, LogRequestMiddleware
from pablog_api.settings.app import get_app_settings

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse


settings = get_app_settings()
configure_logger(settings)

DOCS_URL = "/docs/openapi" if settings.is_development() else None
OPENAPI_URL = "/docs/openapi.json" if settings.is_development() else None


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database(settings.postgres, debug=settings.is_development())
    await init_cache(settings.cache, settings.app_name)

    yield
    await close_database()


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

app.add_middleware(LogRequestMiddleware)
app.add_middleware(AddRequestIDMiddleware, environment=settings.environment)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)

app.include_router(api_router)
