from fastapi.routing import APIRouter

from app.application.api.v1.messages.handlers import router as message_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(message_router)
