from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes): ...

    @abstractmethod
    async def start_consuming(self, topic: str): ...

    @abstractmethod
    async def consume(self, topic: str) -> dict: ...

    @abstractmethod
    async def stop_consuming(self): ...
