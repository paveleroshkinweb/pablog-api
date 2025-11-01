from enum import StrEnum

from pablog_api.settings.base import BaseAppSettings

import pydantic


class BlobStorageType(StrEnum):
    FS_STORAGE = "FS_STORAGE"


class BlobSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "blob_"

    storage_type: BlobStorageType = pydantic.Field(default=BlobStorageType.FS_STORAGE)

    fs_path: str = pydantic.Field(default="/var/www/pablog/uploads/")
