from pablog_api.schema.base import PablogBaseSchema

from pydantic import Field


class HealthCheckResponse(PablogBaseSchema):
    pass


class InfoResponse(PablogBaseSchema):

    version: str = Field(..., description="Application version", examples=["1.0.0"])
