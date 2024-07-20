from punq import Container
from pytest import fixture

from app.infra.repositories.messages.base import BaseChatsRepository
from app.logic.mediator.mediator import Mediator
from app.tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)
