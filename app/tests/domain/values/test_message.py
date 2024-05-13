from datetime import datetime

import pytest

from app.domain.entities.messages import (
    Chat,
    Message,
)
from app.domain.events.messages import NewMessageReceivedEvent
from app.domain.exceptions.messages import (
    EmptyTextException,
    TextTooLongException,
)
from app.domain.values.messages import (
    Text,
    Title,
)


def test_create_message_success():
    text = Text("Hello, world")
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_text_too_long():
    with pytest.raises(TextTooLongException):
        Text("Hello, world" * 150)


def test_create_message_text_empty():
    with pytest.raises(EmptyTextException):
        Text("")


def test_create_chat_success():
    title = Title("Hello, world")
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TextTooLongException):
        Title("Hello, world" * 150)


def test_create_chat_title_empty():
    with pytest.raises(EmptyTextException):
        Title("")


def test_add_chat_to_message():
    text = Text("Hello, world")
    message = Message(text=text)

    title = Title("Hello, world")
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages


def test_new_message_events():
    text = Text("Hello, world")
    message = Message(text=text)

    title = Title("Hello, world")
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events
    assert len(events) == 1, events
    new_events = events[0]

    assert isinstance(new_events, NewMessageReceivedEvent), new_events
    assert new_events.message_text == message.text.as_generic_type()
    assert new_events.chat_oid == chat.oid
    assert new_events.message_oid == message.oid
