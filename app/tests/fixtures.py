from punq import (
    Container,
    Scope,
)

from app.infra.repositories.messages.base import BaseChatRepository
from app.infra.repositories.messages.memory import MemoryChatRepository
from app.logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)

    return container
