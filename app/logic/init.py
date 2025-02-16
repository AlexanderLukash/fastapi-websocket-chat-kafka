from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)


from app.domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
    ChatDeletedEvent,
)
from app.infra.message_brokers.base import BaseMessageBroker
from app.infra.message_brokers.kafka import KafkaMessageBroker
from app.infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.infra.repositories.messages.mongo import (
    MongoDBChatsRepository,
    MongoDBMessagesRepository,
)
from app.infra.websockets.managers import BaseConnectionManager, ConnectionManager
from app.logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
    DeleteChatCommandHandler,
    DeleteChatCommand,
)
from app.logic.events.messages import (
    NewChatCreatedEventHandler,
    NewMessageReceivedEventHandler,
    NewMessageReceivedFromBrokerEventHandler,
    NewMessageReceivedFromBrokerEvent,
    ChatDeleteEventHandler,
)
from app.logic.mediator.base import Mediator
from app.logic.mediator.event import EventMediator
from app.logic.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
    GetAllChatsQuery,
    GetAllChatsQueryHandler,
)
from app.settings.config import Config


@lru_cache(1)
def init_container() -> Container:
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

    def init_chats_mongodb_repository() -> BaseChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_messages_mongodb_repository() -> BaseMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_messages_collection,
        )

    container.register(
        BaseChatsRepository,
        factory=init_chats_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        factory=init_messages_mongodb_repository,
        scope=Scope.singleton,
    )

    # Command handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Query Handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)
    container.register(GetAllChatsQueryHandler)

    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_url,
                group_id=f"chats-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    # Message Broker
    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton,
    )

    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton,
    )

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessagesRepository),
            chat_repository=container.resolve(BaseChatsRepository),
        )
        delete_chat_handler = DeleteChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatsRepository),
        )

        # event handlers
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        new_message_received_handler = NewMessageReceivedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            broker_topic=config.new_messages_received_event_topic,
            connection_manager=container.resolve(BaseConnectionManager),
        )
        new_message_received_from_broker_event_handler = (
            NewMessageReceivedFromBrokerEventHandler(
                message_broker=container.resolve(BaseMessageBroker),
                broker_topic=config.new_messages_received_event_topic,
                connection_manager=container.resolve(BaseConnectionManager),
            )
        )
        chat_deleted_event_handler = ChatDeleteEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            broker_topic=config.chat_deleted_event_topic,
            connection_manager=container.resolve(BaseConnectionManager),
        )

        # Event
        mediator.register_event(
            NewChatCreatedEvent,
            [new_chat_created_event_handler],
        )
        mediator.register_event(
            NewMessageReceivedEvent,
            [new_message_received_handler],
        )
        mediator.register_event(
            NewMessageReceivedFromBrokerEvent,
            [new_message_received_from_broker_event_handler],
        )
        mediator.register_event(
            ChatDeletedEvent,
            [chat_deleted_event_handler],
        )

        # Commands
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )
        mediator.register_command(
            DeleteChatCommand,
            [delete_chat_handler],
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

        mediator.register_query(
            GetAllChatsQuery,
            container.resolve(GetAllChatsQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
