from dataclasses import dataclass

from app.domain.events.messages import NewChatCreatedEvent
from app.infra.message_brokers.converters import convert_event_to_broker_message
from app.logic.events.base import (
    ER,
    ET,
    EventHandler,
)


@dataclass()
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: ET) -> ER:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )
        print(f"Event read successfully: {event.title, event.__class__}.")
