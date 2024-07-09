from pablog_api.schema.base import PablogBaseSchema


class HealthCheckResponse(PablogBaseSchema):
    pass


class InfoResponse(PablogBaseSchema):

    version: str
