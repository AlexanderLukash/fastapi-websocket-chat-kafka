from dataclasses import dataclass
from typing import ClassVar

from app.domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
    ChatDeletedEvent,
    ListenerAddedEvent,
)
from app.infra.message_brokers.converters import convert_event_to_broker_message
from app.logic.events.base import (
    EventHandler,
    IntegrationEvent,
)


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )


@dataclass
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )


@dataclass
class NewMessageReceivedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = "New Message From Broker Received"

    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewMessageReceivedFromBrokerEventHandler(
    EventHandler[NewMessageReceivedFromBrokerEvent, None],
):
    async def handle(self, event: NewMessageReceivedFromBrokerEvent) -> None:
        await self.connection_manager.send_all(
            key=event.chat_oid,
            bytes_=convert_event_to_broker_message(event=event),
        )


@dataclass
class ChatDeleteEventHandler(EventHandler[ChatDeletedEvent, None]):
    async def handle(self, event: ChatDeletedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )
        await self.connection_manager.disconnect_all(event.chat_oid)


@dataclass
class ListenerAddedEventHandler(
    EventHandler[ListenerAddedEvent, None],
):
    async def handle(self, event: ListenerAddedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )
