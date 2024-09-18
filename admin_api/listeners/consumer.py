from aio_pika.abc import AbstractIncomingMessage
import logging
from .book_action import action_update_book
from .user_action import action_create_user

LOGGER = logging.getLogger(__name__)


FRONTEND_ROUTE_KEY = {
    "update_book": action_update_book,
    "create_library_user": action_create_user,
}


async def on_consume(message: AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    LOGGER.info("Consumer job recieved")

    LOGGER.info(" [x] Received message %r" % message.body)
    LOGGER.info(f"messaging : {message.routing_key}")

    if FRONTEND_ROUTE_KEY.get(message.routing_key):
        await FRONTEND_ROUTE_KEY[message.routing_key](message.body)

    LOGGER.info("Consumer job processing completed")
