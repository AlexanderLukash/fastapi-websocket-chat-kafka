from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container

from app.application.api.schemas import ErrorSchema
from app.application.api.v1.messages.filters import GetMessagesFilters, GetChatsFilters
from app.application.api.v1.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
    GetChatsQueryResponseSchema,
    AddTelegramListenerSchema,
    AddTelegramListenerResponseSchema,
    ChatListenersListItemsSchema,
)
from app.domain.exceptions.base import ApplicationException
from app.logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
    DeleteChatCommand,
    AddTelegramListenerCommand,
)
from app.logic.init import init_container
from app.logic.mediator.base import Mediator
from app.logic.queries.messages import (
    GetChatDetailQuery,
    GetMessagesQuery,
    GetAllChatsQuery,
    GetAllChatsListenersQuery,
)

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
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
    container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Create a new chat."""
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
    "/{chat_oid}/messages/",
    status_code=status.HTTP_201_CREATED,
    description="Handle for adding a new message to the chat with the passed ObjectID.",
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
    """Add a new message to the chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(
                text=schema.text,
                source=schema.source,
                chat_oid=chat_oid,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    "/{chat_oid}/",
    status_code=status.HTTP_200_OK,
    description="Get information about the chat and all messages in it.",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_chat_with_messages_handler(
    chat_oid: str,
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
    "/{chat_oid}/messages/",
    status_code=status.HTTP_200_OK,
    description="All sent chat messages.",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="All chat at that moment.",
    responses={
        status.HTTP_200_OK: {"model": GetChatsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_chats_handler(
    filters: GetChatsFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetChatsQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chats, count = await mediator.handle_query(
            GetAllChatsQuery(filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetChatsQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ChatDetailSchema.from_entity(chat) for chat in chats],
    )


@router.delete(
    "/{chat_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete chat after conversation ends.",
    description="Delete chat by provided 'chat_oid'",
)
async def delete_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteChatCommand(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )


@router.post(
    "/{chat_oid}/listeners/",
    status_code=status.HTTP_201_CREATED,
    summary="Add telegram listener to chat.",
    description="Add telegram listener to chat.",
    operation_id="addTelegramListener",
    response_model=AddTelegramListenerResponseSchema,
)
async def add_telegram_listener_handler(
    chat_oid: str,
    schema: AddTelegramListenerSchema,
    container: Container = Depends(init_container),
) -> AddTelegramListenerResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        listener, *_ = await mediator.handle_command(
            AddTelegramListenerCommand(
                chat_oid=chat_oid,
                telegram_chat_id=schema.telegram_chat_id,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return AddTelegramListenerResponseSchema.from_entity(listener)


@router.get(
    "/{chat_oid}/listeners/",
    status_code=status.HTTP_200_OK,
    description="Get all chat listeners.",
    responses={
        status.HTTP_200_OK: {"model": list[ChatListenersListItemsSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_chat_listeners_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> list[ChatListenersListItemsSchema]:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat_listeners = await mediator.handle_query(
            GetAllChatsListenersQuery(chat_oid=chat_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return [
        ChatListenersListItemsSchema.from_entity(listener=chat_listener)
        for chat_listener in chat_listeners
    ]
