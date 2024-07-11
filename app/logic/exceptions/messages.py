from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'A chat with the same name "{self.title}" already exists.'
