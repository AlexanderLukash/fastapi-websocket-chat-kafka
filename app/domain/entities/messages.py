from dataclasses import dataclass

from app.domain.values.messages import Text


@dataclass
class Message:
    oid = str
    text = Text
    