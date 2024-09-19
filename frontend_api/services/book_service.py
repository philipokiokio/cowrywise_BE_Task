import logging
import schemas.book_schemas as schemas
import services.mq_publisher as mq
from services.service_exception import CreateError, NotFoundError, UpdateError
from uuid import UUID
import database.db_handlers.book_db_handler as book_db_handler
from fastapi import HTTPException, status
from datetime import date, datetime, timedelta
import json

LOGGER = logging.getLogger(__name__)


async def get_book(book_uid: UUID):

    try:
        return await book_db_handler.get_book(book_id=book_uid)

    except NotFoundError:

        raise HTTPException(
            detail="book not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def create_book(book: schemas.Book):

    try:
        try:
            await get_book(book_uid=book.book_uid)
        except HTTPException:
            LOGGER.info("creating book record")
            await book_db_handler.create_book(book=book)

    except CreateError:  # noqa: F821
        LOGGER.error(f"book failed to create for {book.model_dump()}")
        pass


async def get_books(**kwargs):
    return await book_db_handler.get_books(**kwargs)


async def update_book(book_uid: UUID, book_update: schemas.BookUpdate):

    book = await get_book(book_uid=book_uid)

    try:

        if book_update.is_borrowed:
            if book.is_borrowed:
                raise HTTPException(
                    detail="book is not available to be borrowed",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            book_update.date_borrowed = date.today()
            book_borrow = schemas.BorrowBook(
                **book_update.model_dump(), book_uid=book_uid
            )
            await book_db_handler.create_borrowed_record(book_borrow=book_borrow)

        updated_book = await book_db_handler.update_book(
            book_id=book_uid, is_borrowed=book_update.is_borrowed
        )
        data = book_update.model_dump()
        data["book_uid"] = str(book_uid)

        data = json.dumps(data, default=str)
        await mq.mq_publish(data=data, routing_key="update_book")

        return updated_book

    except UpdateError:
        raise HTTPException(
            detail="book failed to update",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_book_action():

    book_result_set = await get_books(borrowed_book=True)
    for book in book_result_set.result_set:
        LOGGER.info(book)
        if book.borrow_history:
            borrow_history = book.borrow_history[-1]

            due_date = borrow_history.date_borrowed + timedelta(
                days=borrow_history.duration_borrowed_for
            )
            if datetime.now().date() >= due_date:
                await update_book(
                    book_uid=book.book_uid,
                    book_update=schemas.BookUpdate(is_borrowed=False),
                )
