from typing import (
    Any,
    Mapping,
)

from app.domain.entities.messages import (
    Chat,
    Message,
)
from app.domain.values.messages import (
    Text,
    Title,
)


def convert_message_entity_to_document(message: Message) -> dict:
    return {
        "oid": message.oid,
        "chat_oid": message.chat_oid,
        "text": message.text.as_generic_type(),
        "created_at": message.created_at,
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
    }


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        oid=message_document["oid"],
        chat_oid=message_document["chat_oid"],
        text=Text(value=message_document["text"]),
        created_at=message_document["created_at"],
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        oid=chat_document["oid"],
        title=Title(value=chat_document["title"]),
        created_at=chat_document["created_at"],
    )
