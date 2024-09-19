from faker import Faker
from schemas import user_schemas, book_schemas
from uuid import uuid4, UUID
from datetime import date, datetime
from random import randint

faker = Faker()


faker["en_US"]


def get_user(user_uid: UUID):
    return user_schemas.User(
        user_uid=user_uid,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
    )


def get_user_profile(user: user_schemas.User):

    return user_schemas.UserProfile(
        date_created_utc=datetime.utcnow(), **user.model_dump()
    )


def get_book():
    return book_schemas.Book(
        title=faker.street_name(),
        author=faker.name(),
        publisher=faker.company(),
        category=faker.name(),
        admin_uid=uuid4(),
    )


def get_book_profile(
    book: book_schemas.Book, book_uid: UUID, admin_uid: UUID, is_borrowed: bool = False
):

    return book_schemas.BookProfile(
        book_uid=book_uid,
        is_borrowed=is_borrowed,
        admin_uid=admin_uid,
        **book.model_dump()
    )


def get_borrow_book(book_uid: UUID, borrowed_by: UUID):
    return book_schemas.BorrowBook(
        date_borrowed=date.today(),
        duration_borrowed_for=randint(0, 4),
        book_uid=book_uid,
        borrowed_by=borrowed_by,
    )


def get_book_update(is_borrowed: bool, borrowed_by: UUID, book_uid: UUID):
    return book_schemas.BookUpdate(
        book_uid=book_uid,
        date_borrowed=date.today(),
        duration_borrowed_for=randint(0, 4),
        is_borrowed=is_borrowed,
        borrowed_by=borrowed_by,
    )


def get_borrow_book_profile(borrow_book: book_schemas.BorrowBook, uid: UUID):
    return book_schemas.BorrowBookProfile(uid=uid, **borrow_book.model_dump())
