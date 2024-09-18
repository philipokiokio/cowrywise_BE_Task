from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from root.api_router import router
import logging

from aio_pika import connect
from root.settings import Settings
from listeners.consumer import on_consume


# Configure the logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Customize log format
    handlers=[logging.StreamHandler()],  # Output logs to the console
)

# Create the logger
LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def mq_life_span(app: FastAPI):
    # Perform connection
    connection = await connect(url=str(Settings().ampq_url))
    LOGGER.info("AMPQ started")
    async with connection:
        # Creating a channel
        channel = await connection.channel()
        exchange = await channel.declare_exchange("admin_exchange", "direct")

        admin_to_frontend = await channel.declare_queue("admin_to_frontend")

        await admin_to_frontend.bind(exchange=exchange, routing_key="create_book")
        await admin_to_frontend.consume(callback=on_consume, no_ack=True)

        yield
    LOGGER.info("AMPQ ended")


def intialize() -> FastAPI:
    app = FastAPI(lifespan=mq_life_span)
    app.include_router(router=router)

    return app


app = intialize()


@app.get("/", status_code=307)
def root():
    return RedirectResponse(url="/docs")
