from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

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
    await websocket.accept()
    config: Config = container.resolve(Config)

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start_consuming(
        topic=config.new_messages_received_event_topic.format(chat_oid=chat_oid),
    )

    while True:
        try:
            await websocket.send_json(await message_broker.consume)
        finally:
            await message_broker.stop_consuming()
            await websocket.close(reason="Disconnected.")
