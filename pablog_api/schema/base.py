from pydantic import BaseModel, ConfigDict


class PablogBaseSchema(BaseModel):

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
