from dataclasses import (
    dataclass,
    field,
)

from app.domain.entities.base import BaseEntity
from app.domain.events.messages import NewMessageReceivedEvent
from app.domain.values.messages import (
    Text,
    Title,
)


@dataclass
class Message(BaseEntity):
    text: Text

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Message") -> bool:
        return self.oid == __value.oid


@dataclass
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Chat") -> bool:
        return self.oid == __value.oid

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                message_oid=message.oid,
                chat_oid=self.oid,
            ),
        )
