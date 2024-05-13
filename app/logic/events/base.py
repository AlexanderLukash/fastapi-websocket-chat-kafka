from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    TypeVar,
)

from app.domain.events.base import BaseEvent


ET = TypeVar(name="ET", bound=BaseEvent)
ER = TypeVar(name="ER", bound=Any)


@dataclass
class EventHandler[ET, ER](ABC, ET):
    def handle(self, event: ET) -> ER: ...
