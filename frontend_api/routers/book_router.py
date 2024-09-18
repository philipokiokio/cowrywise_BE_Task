import services.book_service as book_service
import schemas.book_schemas as schema
from fastapi import APIRouter, status, Depends
from uuid import UUID

api_router = APIRouter(prefix="/v1/book", tags=["Book Service"])


@api_router.get(
    "s", status_code=status.HTTP_200_OK, response_model=schema.PaginatedBookProfile
)
async def get_books(book_filter: schema.BookFilter = Depends(schema.BookFilter)):
    return await book_service.get_books(**book_filter.model_dump())


@api_router.get(
    "/{book_uid}", status_code=status.HTTP_200_OK, response_model=schema.BookProfile
)
async def get_book(book_uid: UUID):
    return await book_service.get_book(book_uid=book_uid)


@api_router.patch(
    "/{book_uid}", status_code=status.HTTP_200_OK, response_model=schema.BookProfile
)
async def update_book(book_uid: UUID, book_update: schema.BookUpdate):
    return await book_service.update_book(book_uid=book_uid, book_update=book_update)
