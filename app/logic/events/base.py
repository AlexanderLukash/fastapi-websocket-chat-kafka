from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from app.domain.events.base import BaseEvent
from app.infra.message_brokers.base import BaseMessageBroker


ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None
    message_broker: BaseMessageBroker

    def handle(self, event: ET) -> ER: ...
