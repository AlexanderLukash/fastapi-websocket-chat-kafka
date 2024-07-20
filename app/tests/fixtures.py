from punq import (
    Container,
    Scope,
)

from app.infra.repositories.messages.base import BaseChatsRepository
from app.infra.repositories.messages.memory import MemoryChatsRepository
from app.logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseChatsRepository,
        MemoryChatsRepository,
        scope=Scope.singleton,
    )

    return container
