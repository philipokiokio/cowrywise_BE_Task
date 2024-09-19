from unittest.mock import patch, AsyncMock, Mock
import pytest
from fastapi import HTTPException
from schemas import book_schemas
from services.service_exception import NotFoundError
import tests.utils as general_utils
from uuid import uuid4
import services.book_service as book_service
import json


@patch("services.book_service.book_db_handler")
async def test_get_book_happy_path(mock_book_db):
    book = general_utils.get_book()
    book_profile = general_utils.get_book_profile(book=book, is_borrowed=False)
    mock_book_db.get_book = AsyncMock(return_value=book_profile)

    fetched_book_profile = await book_service.get_book(book_uid=book.book_uid)
    mock_book_db.get_book.assert_called_with(book_id=book.book_uid)
    assert fetched_book_profile == book_profile


@patch("services.book_service.book_db_handler")
async def test_get_book_sad_path(mock_book_db):
    book = general_utils.get_book()
    mock_book_db.get_book = AsyncMock(side_effect=NotFoundError)

    with pytest.raises(HTTPException):
        await book_service.get_book(book_uid=book.book_uid)


@patch("services.book_service.book_db_handler")
async def test_create_book_happy_path(mock_book_db):
    book = general_utils.get_book()
    book_profile = general_utils.get_book_profile(book=book, is_borrowed=False)
    mock_book_db.get_book = AsyncMock(side_effect=NotFoundError)
    mock_book_db.create_book = AsyncMock(return_value=book_profile)

    await book_service.create_book(book=book)
    mock_book_db.create_book.assert_awaited_once_with(book=book)
    mock_book_db.get_book.assert_awaited_once_with(book_id=book.book_uid)


@patch("services.book_service.book_db_handler")
async def test_create_book_sad_path(mock_book_db):
    book = general_utils.get_book()
    book_profile = general_utils.get_book_profile(book=book, is_borrowed=False)
    mock_book_db.get_book = AsyncMock(side_effect=book_profile)

    proof = await book_service.create_book(book=book)
    mock_book_db.get_book.assert_awaited_once_with(book_id=book.book_uid)
    assert proof is None


@patch("services.book_service.book_db_handler")
async def test_get_books_happy_path(mock_book_db):
    book_profile_set = []

    for i in range(5):

        book = general_utils.get_book()
        book_profile_set.append(
            general_utils.get_book_profile(book=book, is_borrowed=False)
        )

    mock_book_db.get_books = AsyncMock(
        return_value=book_schemas.PaginatedBookProfile(
            result_set=book_profile_set, result_size=len(book_profile_set)
        )
    )

    book_profiles = await book_service.get_books()

    assert book_profile_set == book_profiles.result_set
    assert len(book_profile_set) == book_profiles.result_size


@patch("services.book_service.book_db_handler")
async def test_get_books_sad_path(mock_book_db):
    book_profile_set = []

    mock_book_db.get_books = AsyncMock(return_value=book_schemas.PaginatedBookProfile())

    book_profiles = await book_service.get_books()

    assert book_profile_set == book_profiles.result_set
    assert len(book_profile_set) == book_profiles.result_size


@patch("services.book_service.book_db_handler")
@patch("services.book_service.mq")
async def test_update_book_happy_path(mock_mq, mock_book_db):

    book = general_utils.get_book()
    book_profile = general_utils.get_book_profile(book=book, is_borrowed=False)
    mocke_updated_book = general_utils.get_book_profile(book=book, is_borrowed=True)

    mock_book_db.get_book = AsyncMock(return_value=book_profile)
    book_update = general_utils.get_book_update(is_borrowed=True, borrowed_by=uuid4())

    mock_book_db.update_book = AsyncMock(return_value=mocke_updated_book)

    mock_book_db.create_borrowed_record = AsyncMock(return_value=None)
    mock_mq.mq_publish = AsyncMock(return_value=None)

    update_book_profile = await book_service.update_book(
        book_uid=book.book_uid, book_update=book_update
    )
    book_borrow = general_utils.get_borrow_book(
        book_uid=book.book_uid, borrowed_by=book_update.borrowed_by
    )
    book_borrow.duration_borrowed_for = book_update.duration_borrowed_for
    mock_book_db.get_book.assert_awaited_once_with(book_id=book.book_uid)
    mock_book_db.update_book.assert_awaited_once_with(
        book_id=book.book_uid, is_borrowed=book_update.is_borrowed
    )
    mock_book_db.create_borrowed_record.assert_awaited_once_with(
        book_borrow=book_borrow
    )
    data = book_update.model_dump()
    data["book_uid"] = str(book.book_uid)

    data = json.dumps(data, default=str)
    mock_mq.mq_publish.assert_awaited_once_with(data=data, routing_key="update_book")
    assert update_book_profile.is_borrowed != book_profile.is_borrowed


@patch("services.book_service.book_db_handler")
async def test_update_book_one_sad_path(mock_book_db):

    book = general_utils.get_book()
    book_profile = general_utils.get_book_profile(book=book, is_borrowed=True)

    mock_book_db.get_book = AsyncMock(return_value=book_profile)
    book_update = general_utils.get_book_update(is_borrowed=True, borrowed_by=uuid4())

    with pytest.raises(HTTPException):
        await book_service.update_book(book_uid=book.book_uid, book_update=book_update)


@patch("services.book_service.book_db_handler")
async def test_update_book_two_sad_path(mock_book_db):

    book = general_utils.get_book()

    mock_book_db.get_book = AsyncMock(side_effect=NotFoundError)
    book_update = general_utils.get_book_update(is_borrowed=True, borrowed_by=uuid4())

    with pytest.raises(HTTPException):
        await book_service.update_book(book_uid=book.book_uid, book_update=book_update)
