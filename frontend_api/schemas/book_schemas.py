from root.utils.base_schemas import AbstractModel, PaginatedQuery
from uuid import UUID
from typing import Optional
from datetime import date
from pydantic import conint


class Book(AbstractModel):
    book_uid: UUID
    title: str
    author: str
    publisher: str
    category: str
    admin_uid: UUID


class BorrowBook(AbstractModel):
    book_uid: UUID
    date_borrowed: date
    duration_borrowed_for: int
    borrowed_by: UUID


class BookProfile(Book):
    is_borrowed: Optional[bool] = None
    borrow_history: list[BorrowBook] = []


class PaginatedBookProfile(AbstractModel):
    result_set: list[BookProfile] = []
    result_size: conint(ge=0) = 0


class BookUpdate(AbstractModel):
    is_borrowed: Optional[bool] = None
    date_borrowed: Optional[date] = None
    duration_borrowed_for: Optional[int] = None
    borrowed_by: Optional[UUID] = None


class BookFilter(PaginatedQuery):
    publisher: Optional[str] = None
    category: Optional[str] = None


class BorrowBook(AbstractModel):
    book_uid: UUID
    date_borrowed: date
    duration_borrowed_for: int
    borrowed_by: UUID


class BorrowBookProfile(BorrowBook):
    uid: UUID
