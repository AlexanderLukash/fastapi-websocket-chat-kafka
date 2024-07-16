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
