from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from motor.core import AgnosticClient

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
from app.infra.repositories.messages.converters import (
    convert_chat_document_to_entity,
    convert_chat_entity_to_document,
    convert_message_document_to_entity,
    convert_message_entity_to_document,
    convert_chat_listener_document_to_entity,
)


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):
    async def check_chat_exists_by_oid(self, oid: str) -> bool:
        return bool(
            await self._collection.find_one(
                filter={"oid": oid},
            ),
        )

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(
            await self._collection.find_one(
                filter={"title": title},
            ),
        )

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={"oid": oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))

    async def delete_chat_by_oid(self, chat_oid: str) -> None:
        await self._collection.delete_one(filter={"oid": chat_oid})

    async def get_all_chats(
        self,
        filters: GetAllChatsFilters,
    ) -> tuple[Iterable[Chat], int]:
        cursor = self._collection.find().skip(filters.offset).limit(filters.limit)
        count = await self._collection.count_documents({})
        chats = [
            convert_chat_document_to_entity(chat_document=chat_document)
            async for chat_document in cursor
        ]

        return chats, count

    async def add_telegram_listener(self, chat_oid: str, telegram_chat_id: str):
        await self._collection.update_one(
            {"oid": chat_oid},
            {"$push": {"listeners": telegram_chat_id}},
            upsert=True,
        )

    async def get_listeners(self, chat_oid: str) -> Iterable[ChatListener]:
        chat = await self.get_chat_by_oid(oid=chat_oid)

        return [
            convert_chat_listener_document_to_entity(listener_id=listener.oid)
            for listener in chat.listeners
        ]


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_entity_to_document(message),
        )

    async def get_messages(
        self,
        chat_oid: str,
        filters: GetMessagesFilters,
    ) -> tuple[Iterable[Message], int]:
        find = {"chat_oid": chat_oid}
        cursor = self._collection.find(find).skip(filters.offset).limit(filters.limit)
        count = await self._collection.count_documents(filter=find)
        messages = [
            convert_message_document_to_entity(message_document=message_document)
            async for message_document in cursor
        ]

        return messages, count
