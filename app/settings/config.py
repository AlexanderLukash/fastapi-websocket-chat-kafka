from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_chat_database: str = Field(default="chat", alias="MONGO_DB_CHAT_DATABASE")
    mongodb_chat_collection: str = Field(
        default="chat",
        alias="MONGO_DB_CHAT_COLLECTION",
    )
    mongodb_messages_collection: str = Field(
        default="messages",
        alias="MONGO_DB_MESSAGE_COLLECTION",
    )
    kafka_url: str = Field(default="kafka:29092", alias="KAFKA_URL")

    new_chats_event_topic: str = Field(default="new-chats-topic")
    new_messages_received_event_topic: str = Field(
        default="new-messages-topic",
    )
