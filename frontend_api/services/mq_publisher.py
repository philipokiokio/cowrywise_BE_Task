from aio_pika import Message, connect
from root.settings import Settings
import logging

LOGGER = logging.getLogger()


async def mq_publish(data: str, routing_key: str):

    # Perform connection
    connection = await connect(str(Settings().ampq_url))

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        exchange = await channel.declare_exchange("frontend_exchange", "direct")

        data = data.encode(encoding="utf-8")
        LOGGER.info(f"Data published to routing_key: {routing_key}, with data: {data}")
        await exchange.publish(Message(data), routing_key=routing_key)
        LOGGER.info("Message published")
