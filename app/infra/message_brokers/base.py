from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    # consumer: AIOKafkaConsumer

    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes): ...

    @abstractmethod
    async def consume(self, topic: str): ...
