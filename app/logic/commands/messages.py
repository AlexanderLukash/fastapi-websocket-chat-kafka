from dataclasses import dataclass

from app.domain.entities.messages import (
    Chat,
    Message,
)
from app.domain.values.messages import (
    Text,
    Title,
)
from app.infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.logic.commands.base import (
    BaseCommand,
    CommandHandler,
)
from app.logic.exceptions.messages import (
    ChatNotFoundException,
    ChatWithThatTitleAlreadyExistsException,
)


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)

        new_chat = Chat.create_chat(title=title)
        await self.chat_repository.add_chat(new_chat)
        self._mediator.publish(new_chat.pull_events())

        return new_chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Chat]):
    chat_repository: BaseChatsRepository
    message_repository: BaseMessagesRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chat_repository.get_chat_by_oid(oid=command.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        message = Message(text=Text(value=command.text), chat_oid=command.chat_oid)
        chat.add_message(message)
        await self.message_repository.add_message(
            message=message,
        )
        return message
