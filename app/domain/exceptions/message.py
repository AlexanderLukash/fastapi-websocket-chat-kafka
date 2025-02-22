from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Message text is too long "{self.text[:255]}..."'


@dataclass(eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return "Text cannot be empty"


@dataclass(eq=False)
class ListenerAlreadyExistsException(ApplicationException):
    listener_id: str

    @property
    def message(self):
        return "Listener already exists."
