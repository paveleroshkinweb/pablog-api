from pablog_api.schema.base import PablogBaseSchema


class ConfigurationBodySchema(PablogBaseSchema):
    pass


class ConfigurationSchema(PablogBaseSchema):

    id: int
    data: ConfigurationBodySchema
