from celery import Celery
from root.settings import Settings
from celery.schedules import crontab
import services.book_service as book_service
import asyncio


redis_url = str(Settings().redis_url)

app = Celery(
    "root",
    broker=redis_url,
    broker_connection_retry_on_startup=True,
)


@app.task
def update_returned_books():

    loop = asyncio.get_event_loop()
    loop.run_until_complete(book_service.update_book_action())


app.add_periodic_task(
    crontab(0, 0),
    update_returned_books.s(),
    name="Update Books",
)
