from dataclasses import dataclass
from typing import (
    Generic,
    Iterable,
)

from app.domain.entities.messages import (
    Chat,
    Message,
    ChatListener,
)
from app.infra.repositories.filters.messages import (
    GetMessagesFilters,
    GetAllChatsFilters,
)
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
class GetAllChatsQuery(BaseQuery):
    filters: GetAllChatsFilters


@dataclass(frozen=True)
class GetAllChatsQueryHandler(BaseQueryHandler[GetAllChatsQuery, Iterable[Chat]]):
    chat_repository: BaseChatsRepository

    async def handle(self, query: GetAllChatsQuery) -> tuple[Iterable[Chat], int]:
        return await self.chat_repository.get_all_chats(
            filters=query.filters,
        )


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> tuple[Iterable[Message], int]:
        return await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )


@dataclass(frozen=True)
class GetAllChatsListenersQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetAllChatsListenersQueryHandler(
    BaseQueryHandler[GetAllChatsListenersQuery, Iterable[ChatListener]],
):
    chat_repository: BaseChatsRepository

    async def handle(self, query: GetAllChatsListenersQuery) -> Iterable[ChatListener]:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        listeners = await self.chat_repository.get_listeners(chat_oid=query.chat_oid)
        return listeners
