from pablog_api.schema.base import PablogBaseSchema

from pydantic import Field


class ErrorResponse(PablogBaseSchema):

    message: str = Field(..., description="Message about what went wrong", examples=["Oops, something went wrong"])
