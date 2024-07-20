from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from app.infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer = AIOKafkaProducer

    async def send_message(self, topic: str, message: str):
        await self.producer.send_and_wait(
            topic=topic,
            value=message,
        )

    async def consume_messages(self, topic: str): ...
