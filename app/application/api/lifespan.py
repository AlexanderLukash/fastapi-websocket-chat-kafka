from app.infra.message_brokers.base import BaseMessageBroker
from app.logic.events.messages import NewMessageReceivedFromBrokerEvent
from app.logic.init import init_container
from app.logic.mediator.base import Mediator
from app.settings.config import Config


async def init_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def consume_in_background():
    container = init_container()
    config: Config = container.resolve(Config)
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    mediator: Mediator = container.resolve(Mediator)

    async for msg in message_broker.start_consuming(
        config.new_messages_received_event_topic,
    ):  # noqa
        await mediator.publish(
            [
                NewMessageReceivedFromBrokerEvent(
                    message_text=msg["message_text"],
                    message_oid=msg["message_oid"],
                    chat_oid=msg["chat_oid"],
                ),
            ],
        )


async def close_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()
