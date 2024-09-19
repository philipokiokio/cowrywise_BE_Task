from database.db_handlers import user_db_handler, book_db_handler
from schemas.user_schemas import User
from schemas.book_schemas import Book
from uuid import UUID


async def create_user(user: User):

    return await user_db_handler.create_user(user=user)


async def create_book(book: Book, admin_uid: UUID):
    return await book_db_handler.create_book(book=book, admin_uid=admin_uid)
