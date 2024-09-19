from unittest.mock import patch, AsyncMock

from root.app import app
import tests.utils as general_utils

from uuid import uuid4
from fastapi.testclient import TestClient
import json
from fastapi import HTTPException, status


import schemas.book_schemas as schemas


TEST_CLIENT = TestClient(app=app)


@patch("routers.book_route.book_service")
async def test_get_books_happy_path(mock_book_service):
    book_result_set = []
    admin_uid = uuid4()
    for i in range(5):
        book_uid = uuid4()
        book = general_utils.get_book()
        book_profile = general_utils.get_book_profile(
            book=book, is_borrowed=False, book_uid=book_uid, admin_uid=admin_uid
        )

        book_result_set.append(book_profile)

    mock_book_service.get_books = AsyncMock(
        return_value=schemas.PaginatedBookProfile(
            result_set=book_result_set, result_size=len(book_result_set)
        ).model_dump()
    )

    response = TEST_CLIENT.get(
        url="/v1/books", params=schemas.BookFilter().model_dump()
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(
        schemas.PaginatedBookProfile(
            result_set=book_result_set, result_size=len(book_result_set)
        ).model_dump_json()
    )


@patch("routers.book_route.book_service")
async def test_get_book_sad_path(mock_book_service):

    mock_book_service.get_books = AsyncMock(
        return_value=schemas.PaginatedBookProfile().model_dump()
    )

    params = schemas.BookFilter().model_dump()
    response = TEST_CLIENT.get(url="/v1/books", params=params)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(schemas.PaginatedBookProfile().model_dump_json())


@patch("routers.book_route.book_service")
async def test__get_book_happy_path(mock_book_service):
    book_uid = uuid4()
    admin_uid = uuid4()
    book = general_utils.get_book()
    book_profile = general_utils.get_book_profile(
        book=book, is_borrowed=False, admin_uid=admin_uid, book_uid=book_uid
    )
    mock_book_service.get_book = AsyncMock(return_value=book_profile.model_dump())

    response = TEST_CLIENT.get(url=f"/v1/book/{book_uid}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(book_profile.model_dump_json())
    mock_book_service.get_book.assert_awaited_once_with(book_uid=book_uid)


@patch("routers.book_route.book_service")
async def test_get__book_sad_path(mock_book_service):
    book_uid = uuid4()
    mock_book_service.get_book.side_effect = HTTPException(
        status_code=404, detail="book not found"
    )

    response = TEST_CLIENT.get(url=f"/v1/book/{book_uid}")
    response_json = response.json()
    assert response.status_code == 404
    assert response_json == {"detail": "book not found"}


@patch("routers.book_route.book_service")
async def test_create_book_happy_path(mock_book_service):

    book = general_utils.get_book()
    admin_uid, book_uid = uuid4(), uuid4()
    book_profile = general_utils.get_book_profile(
        book=book, is_borrowed=True, admin_uid=admin_uid, book_uid=book_uid
    )
    book_payload = json.loads(book.model_dump_json())

    mock_book_service.create_book = AsyncMock(return_value=book_profile.model_dump())
    response = TEST_CLIENT.post(url="/v1/book", json=book_payload)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json == json.loads(book_profile.model_dump_json())


@patch("routers.book_route.book_service")
async def test_create__book_sad_path(mock_book_service):
    book = general_utils.get_book()
    mock_book_service.create_book.side_effect = HTTPException(
        detail="book exists",
        status_code=status.HTTP_400_BAD_REQUEST,
    )

    book_payload = json.loads(book.model_dump_json())

    response = TEST_CLIENT.post(url="/v1/book", json=book_payload)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json == {"detail": "book exists"}
