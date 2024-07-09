from pablog_api.schema.response import HealthCheckResponse, InfoResponse
from pablog_api.settings.app import get_app_settings

from fastapi import APIRouter, status


settings = get_app_settings()

router = APIRouter(tags=["utils"])


@router.get(
    path="/healthcheck",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
    summary="Check either the service is up and running"
)
def healthcheck() -> HealthCheckResponse:
    return HealthCheckResponse()


@router.get(
    path="/info",
    status_code=status.HTTP_200_OK,
    response_model=InfoResponse,
    summary="Get the basic information about the service"
)
def info() -> InfoResponse:
    return InfoResponse(version=settings.app_version)
