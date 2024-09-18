import services.book_service as book_service
import schemas.book_schemas as schema
from fastapi import APIRouter, status, Depends
from uuid import UUID, uuid4

api_router = APIRouter(prefix="/v1/book", tags=["Book Service"])


@api_router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schema.BookProfile
)
async def create_book(book: schema.Book, admin_uid: UUID = Depends(uuid4)):
    return await book_service.create_book(book=book, admin_uid=admin_uid)


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
