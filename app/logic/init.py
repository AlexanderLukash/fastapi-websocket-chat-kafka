from app.infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from app.logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
):
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)],
    )
