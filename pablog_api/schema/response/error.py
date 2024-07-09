from pablog_api.schema.base import PablogBaseSchema

from pydantic import Field


class ErrorResponse(PablogBaseSchema):

    request_id: str = Field(..., description="Related request id", examples=["550e8400-e29b-41d4-a716-446655440000"])
    message: str = Field(..., description="Message about what went wrong", examples=["Oops, something went wrong"])
