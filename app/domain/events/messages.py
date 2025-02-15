from dataclasses import dataclass
from typing import ClassVar

from app.domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    event_title: ClassVar[str] = "New Message Received"

    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New Chat Created"

    chat_oid: str
    chat_title: str


@dataclass
class ChatDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Chat has been deleted"

    chat_oid: str
