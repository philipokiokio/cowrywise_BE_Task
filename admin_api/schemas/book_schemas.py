from root.utils.base_schemas import AbstractModel, PaginatedQuery
from uuid import UUID
from typing import Optional
from datetime import date
from pydantic import conint


class Book(AbstractModel):
    title: str
    author: str
    publisher: str
    category: str


class TransportBook(Book):
    book_uid: UUID
    admin_uid: UUID


class BorrowBook(AbstractModel):
    book_uid: UUID
    date_borrowed: date
    duration_borrowed_for: int
    borrowed_by: UUID


class BookProfile(TransportBook):
    is_borrowed: Optional[bool] = None
    date_borrowed: Optional[date] = None
    duration_borrowed_for: Optional[int] = None
    borrowed_by: Optional[UUID] = None
    borrow_history: list[BorrowBook] = []


class PaginatedBookProfile(AbstractModel):
    result_set: list[BookProfile] = []
    result_size: conint(ge=0) = 0


class BookUpdate(AbstractModel):
    book_uid: UUID
    is_borrowed: Optional[bool] = None
    date_borrowed: Optional[date] = None
    duration_borrowed_for: Optional[int] = None
    borrowed_by: Optional[UUID] = None


class BorrowBookProfile(BorrowBook):
    uid: UUID
    book : Optional[BookProfile] = None

class BookFilter(PaginatedQuery):
    publisher: Optional[str] = None
    category: Optional[str] = None
