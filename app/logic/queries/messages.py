from dataclasses import dataclass
from typing import Generic

from app.domain.entities.messages import Chat
from app.infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.logic.exceptions.messages import ChatNotFoundException
from app.logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QR,
    QT,
)


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QT, QR]):
    chat_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat
