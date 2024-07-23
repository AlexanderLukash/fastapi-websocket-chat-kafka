from dataclasses import dataclass
from typing import ClassVar

from app.domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    title: ClassVar[str] = "New Message Received"
    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New Chat Created"
    chat_oid: str
    chat_title: str
