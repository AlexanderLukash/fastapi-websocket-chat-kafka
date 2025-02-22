from datetime import datetime

from pydantic import BaseModel

from app.application.api.schemas import BaseQueryResponseSchema
from app.domain.entities.messages import (
    Chat,
    Message,
    ChatListener,
)


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatResponseSchema":
        return CreateChatResponseSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    iod: str
    text: str

    @classmethod
    def from_entity(cls, message: Message) -> "CreateMessageResponseSchema":
        return CreateMessageResponseSchema(
            iod=message.oid,
            text=message.text.as_generic_type(),
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageDetailSchema":
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
        )


class GetMessagesQueryResponseSchema(BaseQueryResponseSchema):
    items: list[MessageDetailSchema]


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatDetailSchema":
        return ChatDetailSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )


class GetChatsQueryResponseSchema(BaseQueryResponseSchema):
    items: list[ChatDetailSchema]


class AddTelegramListenerSchema(BaseModel):
    telegram_chat_id: str


class AddTelegramListenerResponseSchema(BaseModel):
    listener_id: str

    @classmethod
    def from_entity(cls, listener: ChatListener) -> "AddTelegramListenerResponseSchema":
        return cls(
            listener_id=listener.oid,
        )
