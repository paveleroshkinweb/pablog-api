from abc import ABC, abstractmethod


class BlobStorage(ABC):
    
    @abstractmethod
    async def put(self, key: str, value: bytes, timeout: int) -> str:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
