

from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse, Response


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
