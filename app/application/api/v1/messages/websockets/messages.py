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
    try:
        async for consume_message in message_broker.start_consuming(
            topic=config.new_messages_received_event_topic.format(chat_oid=chat_oid),
        ):
            await websocket.send_json(consume_message)
    except Exception as exception:
        raise exception

    await message_broker.stop_consuming()
    await websocket.close(reason="Disconnected.")
