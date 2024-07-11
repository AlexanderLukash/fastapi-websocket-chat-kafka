from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from app.application.api.schemas import ErrorSchema
from app.application.api.v1.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
)
from app.domain.exceptions.base import ApplicationException
from app.logic.commands.messages import CreateChatCommand
from app.logic.init import init_container
from app.logic.mediator import Mediator


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    # response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates a new chat, if a chat with the same name exists, then a 400 error is returned.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateChatResponseSchema.from_entity(chat)
