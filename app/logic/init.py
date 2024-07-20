from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from app.infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.infra.repositories.messages.mongo import (
    MongoDBChatsRepository,
    MongoDBMessagesRepository,
)
from app.logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from app.logic.mediator.base import Mediator
from app.logic.mediator.event import EventMediator
from app.logic.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from app.settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=Scope.singleton,
    )

    client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongodb_repository():
        return MongoDBChatsRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_message_mongodb_repository():
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_messages_collection,
        )

    container.register(
        BaseChatsRepository,
        factory=init_chat_mongodb_repository,
        scope=Scope.singleton,
    )

    container.register(
        BaseMessagesRepository,
        factory=init_message_mongodb_repository,
        scope=Scope.singleton,
    )

    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Query Handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessagesRepository),
            chat_repository=container.resolve(BaseChatsRepository),
        )

        # commands
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )

        # Queries
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
