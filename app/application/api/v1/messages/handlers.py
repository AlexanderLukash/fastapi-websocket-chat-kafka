from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container

from app.application.api.schemas import ErrorSchema
from app.application.api.v1.messages.filters import GetMessagesFilters
from app.application.api.v1.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from app.domain.exceptions.base import ApplicationException
from app.logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from app.logic.init import init_container
from app.logic.mediator.mediator import Mediator
from app.logic.queries.messages import (
    GetChatDetailQuery,
    GetMessagesQuery,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
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


@router.post(
    "/{chat_oid}/messages",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates a new message in a chat.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    "/{chat_oid}",
    status_code=status.HTTP_200_OK,
    description="Endpoint returns a chat by its oid.",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_chat_handler(
    chat_oid,
    container: Container = Depends(init_container),
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return ChatDetailSchema.from_entity(chat)


@router.get(
    "/{chat_oid}/messages",
    status_code=status.HTTP_200_OK,
    description="Get sent messages in chat.",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages],
    )
