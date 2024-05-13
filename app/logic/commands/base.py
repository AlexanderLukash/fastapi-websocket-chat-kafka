from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    TypeVar,
)


@dataclass(frozen=True)
class BaseCommand(ABC): ...


CT = TypeVar(name="CT", bound=BaseCommand)
CR = TypeVar(name="CR", bound=Any)


@dataclass(frozen=True)
class CommandHandler[CT, CR](ABC, CT):
    @abstractmethod
    def handle(self, command: CT) -> CR: ...
