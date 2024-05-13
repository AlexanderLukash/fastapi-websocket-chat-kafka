from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self) -> str:
        return "Text is empty."


@dataclass(eq=False)
class TextTooLongException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f'Text is too long: "{self.text[:225]}..."'
