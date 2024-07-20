from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from app.domain.events.base import BaseEvent
from app.infra.message_brokers.base import BaseMessageBroker
from app.logic.events.base import (
    ER,
    ET,
    EventHandler,
)


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    message_broker: BaseMessageBroker

    @abstractmethod
    def register_event(
        self,
        event: ET,
        event_handlers: Iterable[EventHandler[ET, ER]],
    ): ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]: ...
