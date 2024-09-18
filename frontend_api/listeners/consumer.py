from aio_pika.abc import AbstractIncomingMessage
import logging
from .book_action import action_create_book

LOGGER = logging.getLogger(__name__)


FRONTEND_ROUTE_KEY = {"create_book": action_create_book}


async def on_consume(message: AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    LOGGER.info("Consumer job recieved")

    LOGGER.info("Message body is: %r" % message.body)
    LOGGER.info(message.routing_key)

    if FRONTEND_ROUTE_KEY.get(message.routing_key):
        print(message.routing_key)

        await FRONTEND_ROUTE_KEY[message.routing_key](message.body)

    LOGGER.info("Consumer job processing completed")
