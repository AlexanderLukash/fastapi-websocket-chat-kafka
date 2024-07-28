from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

from app.application.api.common.websockets.managers import (
    BaseConnectionManager,
    ConnectionManager,
)
from app.infra.message_brokers.base import BaseMessageBroker
from app.logic.init import init_container
from app.settings.config import Config

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@router.websocket("/{chat_oid}/")
async def messages_handler(
    chat_oid: UUID,
    websocket: WebSocket,
    container=Depends(init_container),
):
    config: Config = container.resolve(Config)

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    connection_manager: ConnectionManager = container.resolve(BaseConnectionManager)
    await connection_manager.accept_connection(websocket=websocket, key=str(chat_oid))

    try:
        async for message in message_broker.start_consuming(
            topic=config.new_messages_received_event_topic,
        ):
            await connection_manager.send_all(key=str(chat_oid), json_message=message)
    finally:
        await connection_manager.remove_connection(
            websocket=websocket,
            key=str(chat_oid),
        )
        await message_broker.stop_consuming()

    await websocket.close(reason="Disconnected.")
