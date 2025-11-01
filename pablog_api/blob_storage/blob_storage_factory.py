from pablog_api.blob_storage.fs_storage import FSStorage
from pablog_api.blob_storage.storage import BlobStorage
from pablog_api.exception import PablogException
from pablog_api.settings.blob import BlobSettings, BlobStorageType


def blob_storage_factory(settings: BlobSettings) -> BlobStorage:
    storage_type = settings.storage_type
    if storage_type == BlobStorageType.FS_STORAGE:
        return FSStorage(settings)

    raise PablogException(f"Could not initialize blob storage with provided type: {storage_type}")
