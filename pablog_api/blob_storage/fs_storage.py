import asyncio
import os
import tempfile

from contextlib import suppress

from pablog_api.exception.blob import DeleteBlobException
from pablog_api.settings import BlobSettings

from .storage import BlobStorage


def __write_file(path: str, data: bytes):
    dir_name = os.path.dirname(path)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix="tmp_")
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd_final = os.open(path, flags)
        os.close(fd_final)

        with os.fdopen(fd, 'wb') as tmp_file:
            tmp_file.write(data)
            tmp_file.flush()

        os.replace(temp_path, path)
    except Exception:
        with suppress(Exception):
            os.remove(temp_path)
        with suppress(Exception):
            os.remove(path)
        raise


class FSStorage(BlobStorage):

    def __init__(self, blob_settings: BlobSettings):
        super().__init__()
        self.blob_settings = blob_settings

    async def put(self, key: str, value: bytes, timeout: int):
        absolute_path = os.path.join(self.blob_settings.fs_path, key)
        await asyncio.wait_for(
            asyncio.to_thread(__write_file, absolute_path, value),
            timeout=timeout
        )
        return absolute_path

    async def delete(self, key: str):
        absolute_path = os.path.join(self.blob_settings.fs_path, key)
        try:
            os.remove(absolute_path)
        except FileNotFoundError:
            pass
        except OSError as e:
            raise DeleteBlobException from e
