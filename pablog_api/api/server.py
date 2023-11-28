import logging
import time

from collections.abc import Awaitable, Callable
from datetime import datetime

from pablog_api.logging.setup_logger import configure_logger
from pablog_api.settings.app import get_app_settings

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
    logger = logging.getLogger("pablog_api.access")

    request_id = request.headers.get("X-Request-Id", "")
    if not request_id:
        logger.warning("No X-Request-Id was provided!")

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    str_process_time = str(process_time)

    if request.url.path not in ACCESS_LOGS_BLACKLIST:
        remote_addr = request.scope["client"][0]
        real_remote_addr = request.headers.get("X-Real-IP", "")
        user_agent = request.headers.get("User-Agent", "")
        request_method = request.method
        response_body_size = response.headers["content-length"]
        str_start_time = datetime.utcfromtimestamp(start_time)
        status_code = response.status_code
        url = request.url

        request_body_size = 0
        if hasattr(request, "_body"):
            request_body_size = len(request._body)

        logger.info(f"\
            REMOTE_ADDR: {real_remote_addr or remote_addr},\
            REQUEST_BODY_SIZE: {request_body_size},\
            USER_AGENT: {user_agent},\
            REQUEST_METHOD: {request_method},\
            URL: {url},\
            RESPONSE_STATUS: {status_code},\
            RESPONSE_BODY_SIZE: {response_body_size},\
            START_TIME: {str_start_time},\
            TIME_TOOK: {str_process_time}\
        ")

    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time"] = str_process_time
    return response


@app.get(f"{API_PATH_V1}/status")
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
