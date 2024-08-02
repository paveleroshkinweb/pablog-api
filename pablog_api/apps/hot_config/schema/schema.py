from pablog_api.schema.base import PablogBaseSchema


class ConfigurationSchema(PablogBaseSchema):

    class Config:
        extra = 'forbid'
