from database.orms.book_orm import Book as Book_DB
from database.orms.book_orm import BookBorrowed as BorrowedBook_DB
from root.database import async_session
import logging
import schemas.book_schemas as schemas
from sqlalchemy import insert, select, or_, update, and_
from services.service_exception import (
    CreateError,
    NotFoundError,
)
from sqlalchemy.orm import joinedload
from uuid import UUID

LOGGER = logging.getLogger(__name__)


async def create_book(book: schemas.Book, admin_uid: UUID):

    async with async_session() as session:

        stmt = (
            insert(Book_DB)
            .values(**book.model_dump(), admin_uid=admin_uid)
            .returning(Book_DB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            LOGGER.error(f"book failed to create: {book.model_dump()}")
            await session.rollback()
            raise CreateError

        await session.commit()

        return schemas.BookProfile(**result.as_dict())


async def check_book(title: str):
    async with async_session() as session:
        stmt = select(Book_DB).filter(Book_DB.title == title.capitalize())

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            LOGGER.error(f"book not found for : {title}")

            raise NotFoundError

        return schemas.BookProfile(**result.as_dict())


async def get_book(book_uid: UUID):
    async with async_session() as session:
        stmt = (
            select(Book_DB)
            .filter(Book_DB.book_uid == book_uid)
            .options(joinedload(Book_DB.borrowed))
        )

        result = (await session.execute(statement=stmt)).unique().scalar_one_or_none()

        if result is None:
            LOGGER.error(f"book not found for : {book_uid}")

            raise NotFoundError

        return schemas.BookProfile(**result.as_dict(), borrow_history=result.borrowed)


async def get_books(**kwargs):

    #     * by publishers e.g Wiley, Apress, Manning
    # * by category e.g fiction, technology, science
    publisher = kwargs.get("publisher")
    category = kwargs.get("category")
    limit = kwargs.get("lmit", 50)
    offset = kwargs.get("offset", 0)

    filter_array = []

    if publisher:
        filter_array.append(Book_DB.publisher.icontains(publisher))
    if category:
        filter_array.append(Book_DB.category.icontains(category))

    async with async_session() as session:
        stmt = (
            select(Book_DB)
            .options(joinedload(Book_DB.borrowed))
            .filter(or_(*filter_array))
            .limit(limit=limit)
            .offset(offset=offset)
        )

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        if not result:

            return schemas.PaginatedBookProfile()

        return schemas.PaginatedBookProfile(
            result_set=[
                schemas.BookProfile(**x.as_dict(), borrow_history=x.borrowed)
                for x in result
            ],
            result_size=len(result),
        )


async def update_book(book_id: UUID, is_borrowed: bool):

    async with async_session() as session:
        fetch_stmt = (
            select(Book_DB).filter(Book_DB.book_uid == book_id).with_for_update()
        )

        (await session.execute(statement=fetch_stmt)).scalar_one_or_none()

        stmt = (
            update(Book_DB)
            .filter(Book_DB.book_uid == book_id)
            .values(is_borrowed=is_borrowed)
            .returning(Book_DB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:

            LOGGER.error(
                f"book failed to update for id: {book_id}, with payload : {is_borrowed}"
            )
            await session.rollback()

        await session.commit()

        return schemas.BookProfile(**result.as_dict())


async def create_borrowed_record(book_borrow: schemas.BorrowBook):

    async with async_session() as session:

        stmt = (
            insert(BorrowedBook_DB)
            .values(**book_borrow.model_dump())
            .returning(BorrowedBook_DB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            await session.rollback()
            return

        await session.commit()
        return schemas.BorrowBookProfile(**result.as_dict())
