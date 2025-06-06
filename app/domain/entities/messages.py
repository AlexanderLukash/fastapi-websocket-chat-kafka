from dataclasses import (
    dataclass,
    field,
)

from app.domain.entities.base import BaseEntity
from app.domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
    ChatDeletedEvent,
    ListenerAddedEvent,
)
from app.domain.exceptions.message import ListenerAlreadyExistsException
from app.domain.values.messages import (
    Text,
    Title,
)


@dataclass(eq=False)
class Message(BaseEntity):
    chat_oid: str
    text: Text
    source: str


@dataclass(eq=False)
class ChatListener(BaseEntity): ...


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)
    listeners: set[ChatListener] = field(default_factory=set, kw_only=True)
    is_deleted: bool = field(default=False, kw_only=True)

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreatedEvent(
                chat_oid=new_chat.oid,
                chat_title=new_chat.title.as_generic_type(),
            ),
        )

        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
                source=message.source,
            ),
        )

    def delete(self):
        self.is_deleted = True
        self.register_event(ChatDeletedEvent(chat_oid=self.oid))

    def add_listener(self, listener: ChatListener):
        if listener in self.listeners:
            raise ListenerAlreadyExistsException(listener_id=listener.oid)
        self.listeners.add(listener)
        self.register_event(ListenerAddedEvent(listener_id=listener.oid))
