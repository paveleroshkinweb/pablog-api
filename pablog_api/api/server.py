from pablog_api.settings.app import settings
from pablog_api.utils.setup_logger import configure_logger

from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse, Response


configure_logger(settings)


API_PATH_V1 = "/api/v1"

VERSION = "1.0.0"

app = FastAPI(
    title="PablogAPI",
    docs_url="/docs/openapi",
    openapi_url="/docs/openapi.json",
    default_response_class=ORJSONResponse,
    version=VERSION,
)


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
