from database.db_handlers import user_db_handler, book_db_handler
from schemas.user_schemas import User
from schemas.book_schemas import Book


async def create_user(user: User):

    return await user_db_handler.create_user(user=user)


async def create_book(book: Book):
    return await book_db_handler.create_book(book=book)
