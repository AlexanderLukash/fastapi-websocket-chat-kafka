from pytest import fixture

from app.infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from app.logic.init import init_mediator
from app.logic.mediator import Mediator


@fixture(scope='package')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@fixture(scope='package')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)

    return mediator
