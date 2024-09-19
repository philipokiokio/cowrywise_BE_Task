import uuid
import tests.utils as general_utils


import pytest

from database.db_handlers import book_db_handler
import tests.unit_tests.test_db_handlers.db_test_utils as seeder_db_handler
from services.service_exception import (
    NotFoundError,
    UpdateError,
)


async def test_create_book_happy_path(session):

    book = general_utils.get_book()
    admin_uid = uuid.uuid4()

    book_profile = await book_db_handler.create_book(book=book, admin_uid=admin_uid)

    assert book.author == book_profile.author
    assert book.category == book_profile.category
    assert book.title == book_profile.title


async def test_get_book_happy_path(session):
    book = general_utils.get_book()
    admin_uid = uuid.uuid4()

    book_profile = await seeder_db_handler.create_book(book=book, admin_uid=admin_uid)

    fetched_book_profile = await book_db_handler.get_book(
        book_uid=book_profile.book_uid
    )

    assert fetched_book_profile == book_profile


async def test_get_book_sad_path(session):
    book_uid = uuid.uuid4()

    with pytest.raises(NotFoundError):
        await book_db_handler.get_book(book_uid=book_uid)


async def test_check_book_happy_path(session):
    book = general_utils.get_book()
    admin_uid = uuid.uuid4()
    book.title = book.title.capitalize()
    book_profile = await seeder_db_handler.create_book(book=book, admin_uid=admin_uid)

    fetched_book_profile = await book_db_handler.check_book(title=book_profile.title)

    assert fetched_book_profile == book_profile


async def test_check_book_sad_path(session):
    title = str(uuid.uuid4())

    with pytest.raises(NotFoundError):
        await book_db_handler.check_book(title=title)


async def test_get_book_profiles_happy_path(session):
    book_result_set = []
    admin_uid = uuid.uuid4()
    for i in range(5):

        book = general_utils.get_book()
        book_result_set.append(
            await seeder_db_handler.create_book(book=book, admin_uid=admin_uid)
        )

    paginated_books = await book_db_handler.get_books()

    assert paginated_books.result_size == len(book_result_set)


async def test_get_book_profiles_sad_path(session):
    book_result_set = []

    paginated_books = await book_db_handler.get_books()

    assert paginated_books.result_set == book_result_set
    assert paginated_books.result_size == len(book_result_set)


async def test_update_book_happy_path(session):
    admin_uid = uuid.uuid4()

    book = general_utils.get_book()
    book_profile = await seeder_db_handler.create_book(book=book, admin_uid=admin_uid)

    updated_book_profile = await book_db_handler.update_book(
        book_id=book_profile.book_uid, is_borrowed=True
    )

    assert book_profile.is_borrowed != updated_book_profile.is_borrowed
    assert book_profile.book_uid == updated_book_profile.book_uid


async def test_update_book_sad_path(session):

    with pytest.raises(UpdateError):
        await book_db_handler.update_book(book_id=uuid.uuid4(), is_borrowed=True)


async def test_create_book_borrow_record(session):
    user_uid = uuid.uuid4()
    admin_uid = uuid.uuid4()
    user = general_utils.get_user(user_uid=user_uid)
    user_profile = await seeder_db_handler.create_user(user=user)
    book = general_utils.get_book()
    book_profile = await seeder_db_handler.create_book(book=book, admin_uid=admin_uid)

    book_borrowed = general_utils.get_borrow_book(
        book_uid=book_profile.book_uid, borrowed_by=user_profile.user_uid
    )

    book_borrowed_profile = await book_db_handler.create_borrowed_record(
        book_borrow=book_borrowed
    )
    assert book_borrowed.book_uid == book_borrowed_profile.book_uid
    assert book_borrowed.borrowed_by == book_borrowed_profile.borrowed_by
    assert book_borrowed_profile.date_borrowed == book_borrowed.date_borrowed
    assert (
        book_borrowed_profile.duration_borrowed_for
        == book_borrowed.duration_borrowed_for
    )
