import logging
import schemas.book_schemas as schemas
import services.mq_publisher as mq
from services.service_exception import CreateError, NotFoundError, UpdateError
from uuid import UUID
import database.db_handlers.book_db_handler as book_db_handler
from fastapi import HTTPException, status
import json

LOGGER = logging.getLogger(__name__)


async def get_book(book_uid: UUID):

    try:
        return await book_db_handler.get_book(book_uid=book_uid)

    except NotFoundError:

        raise HTTPException(
            detail="book not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def fetch_book(title: str):

    try:
        return await book_db_handler.check_book(title=title)

    except NotFoundError:

        raise HTTPException(
            detail="book not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def create_book(book: schemas.Book, admin_uid: UUID):

    try:
        try:

            await fetch_book(title=book.title)

        except HTTPException:
            LOGGER.info("creating book record")

            book.title = book.title.capitalize()

            book_profile = await book_db_handler.create_book(
                book=book, admin_uid=admin_uid
            )
            LOGGER.info(book_profile.model_dump())
            data = json.dumps(
                schemas.TransportBook(**book_profile.model_dump()).model_dump(),
                default=str,
            )
            # Publishing to Queue
            await mq.mq_publish(data=data, routing_key="create_book")

            return book_profile

        raise HTTPException(
            detail="book exists", status_code=status.HTTP_400_BAD_REQUEST
        )

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
            book_borrow = schemas.BorrowBook(**book_update.model_dump())
            await book_db_handler.create_borrowed_record(book_borrow=book_borrow)

        updated_book = await book_db_handler.update_book(
            book_id=book_uid, is_borrowed=book_update.is_borrowed
        )

        return updated_book

    except UpdateError:
        raise HTTPException(
            detail="book failed to update",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
