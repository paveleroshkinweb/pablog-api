from abc import ABC, abstractmethod
from typing import Any


KeyT = bytes | str | memoryview
ValueT = bytes | memoryview | str


class CacheStorage(ABC):

    @abstractmethod
    async def get(self, key: KeyT) -> Any:
        pass

    @abstractmethod
    async def set(self, key: KeyT, value: ValueT, ttl_ms: None | int = None):
        pass

    @abstractmethod
    async def delete(self, *keys: KeyT):
        pass

    @abstractmethod
    async def exists(self, *keys: KeyT) -> bool:
        pass
