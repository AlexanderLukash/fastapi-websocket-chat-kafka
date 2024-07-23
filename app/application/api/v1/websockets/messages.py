from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket


router = APIRouter(tags=["chats"])


@router.websocket("{chat_oid}")
async def messages_handler(chat_oid: str, websocket: WebSocket):
    await websocket.accept()
