from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class EventHandlerNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self) -> str:
        return f'Event handler not registered: "{self.event_type}".'


@dataclass(frozen=True, eq=False)
class CommandHandlerNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f'Command handler not registered: "{self.command_type}".'
