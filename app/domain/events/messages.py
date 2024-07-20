from dataclasses import dataclass
from typing import ClassVar

from app.domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str
    title: ClassVar[str] = "New Message Received"


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    chat_title: str
    title: ClassVar[str] = "New Chat Created"
