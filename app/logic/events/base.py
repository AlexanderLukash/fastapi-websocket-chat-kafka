from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from app.domain.events.base import BaseEvent


ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    broker_topic: str | None

    def handle(self, event: ET) -> ER: ...
