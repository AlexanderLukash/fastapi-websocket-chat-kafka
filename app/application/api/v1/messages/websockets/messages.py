from fastapi import (
    Depends,
    WebSocketDisconnect,
)
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

from punq import Container

from app.infra.websockets.managers import BaseConnectionManager
from app.logic.exceptions.messages import ChatNotFoundException
from app.logic.init import init_container
from app.logic.mediator.base import Mediator
from app.logic.queries.messages import GetChatDetailQuery

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    chat_oid: str,
    websocket: WebSocket,
    container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ChatNotFoundException as error:
        await websocket.send_json(data={"error": error.message})
        await websocket.close()

    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)

    await websocket.send_text("You are now connected!")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
