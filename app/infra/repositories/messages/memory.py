from dataclasses import (
    dataclass,
    field,
)

from app.domain.entities.messages import Chat
from app.infra.repositories.messages.base import BaseChatsRepository


@dataclass
class MemoryChatsRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return next(chat for chat in self._saved_chats if chat.oid == oid)
        except StopIteration:
            return None

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat
                    for chat in self._saved_chats
                    if chat.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def check_chat_exists_by_oid(self, oid: str) -> bool:
        try:
            return bool(
                next(chat for chat in self._saved_chats if chat.oid == oid),
            )
        except StopIteration:
            return False
