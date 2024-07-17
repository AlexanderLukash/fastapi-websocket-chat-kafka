from dataclasses import dataclass
from typing import (
    Generic,
    Iterable,
)

from app.domain.entities.messages import (
    Chat,
    Message,
)
from app.infra.repositories.filters.messages import GetMessagesFilters
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


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
