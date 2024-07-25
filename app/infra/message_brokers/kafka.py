from dataclasses import (
    dataclass,
    field,
)

import orjson
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)

from app.infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    consumer_map: dict[str, AIOKafkaConsumer] = field(
        default_factory=dict,
        kw_only=True,
    )

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send_and_wait(key=key, topic=topic, value=value)

    async def start_consuming(self, topic: str):
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        self.consumer.unsubscribe()

    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def start(self):
        await self.producer.start()
        await self.consumer.start()
