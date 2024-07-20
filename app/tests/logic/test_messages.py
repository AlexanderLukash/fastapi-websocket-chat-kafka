import pytest
from faker import Faker

from app.domain.entities.messages import Chat
from app.domain.values.messages import Title
from app.infra.repositories.messages.base import BaseChatsRepository
from app.logic.commands.messages import CreateChatCommand
from app.logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from app.logic.mediator.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
):
    chat: Chat
    chat, *_ = await mediator.handle_command(CreateChatCommand(title=faker.text()))

    assert await chat_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type(),
    )


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
):
    title_text = faker.text()
    chat = Chat(title=Title(title_text))
    await chat_repository.add_chat(chat)

    assert chat in chat_repository._saved_chats

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=title_text))

    assert len(chat_repository._saved_chats) == 1
