from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from app.infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send_and_wait(key=key, topic=topic, value=value)

    async def consume(self, topic: str): ...
