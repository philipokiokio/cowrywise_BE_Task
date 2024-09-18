import uuid
import tests.utils as general_utils


import pytest

from database.db_handlers import book_db_handler
import tests.unit_tests.test_db_handlers.db_test_utils as seeder_db_handler
from services.service_exception import (
    NotFoundError,
    CreateError,
)


async def test_create_book_happy_path(session):

    book = general_utils.get_book()

    book_profile = await book_db_handler.create_book(book=book)

    assert book.book_uid == book_profile.book_uid
    assert book.admin_uid == book_profile.admin_uid
    assert book.author == book_profile.author
    assert book.category == book_profile.category
    assert book.title == book_profile.title


async def test_create_book_sad_path(session):

    book = general_utils.get_book()

    await seeder_db_handler.create_book(book=book)
    with pytest.raises(CreateError):
        await book_db_handler.create_book(book=book)


async def test_get_book_happy_path(session):
    book = general_utils.get_book()

    book_profile = await seeder_db_handler.create_book(book=book)

    fetched_book_profile = await book_db_handler.get_book(book_id=book_profile.book_uid)

    assert fetched_book_profile == book_profile


async def test_get_book_sad_path(session):
    book = general_utils.get_book()
    with pytest.raises(NotFoundError):
        await book_db_handler.get_book(book_id=book.book_uid)


async def test_get_book_profiles_happy_path(session):
    book_result_set = []
    for i in range(5):

        book = general_utils.get_book()
        book_result_set.append(await seeder_db_handler.create_book(book=book))

    paginated_books = await book_db_handler.get_books()

    assert paginated_books.result_set == book_result_set
    assert paginated_books.result_size == len(book_result_set)


async def test_get_book_profiles_sad_path(session):
    book_result_set = []

    paginated_books = await book_db_handler.get_books()

    assert paginated_books.result_set == book_result_set
    assert paginated_books.result_size == len(book_result_set)
