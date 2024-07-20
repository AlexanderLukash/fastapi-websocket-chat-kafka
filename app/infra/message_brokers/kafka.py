from dataclasses import dataclass

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)

from app.infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def send_message(self, topic: str, value: bytes):
        await self.producer.send(topic=topic, value=value)

    async def consume_messages(self, topic: str): ...
