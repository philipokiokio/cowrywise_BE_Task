from faker import Faker
from schemas import user_schemas, book_schemas
from uuid import uuid4
from datetime import date, datetime, timedelta

faker = Faker()


faker["en_US"]


def get_user():
    return user_schemas.User(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
    )


def get_book():
    return book_schemas.Book(
        book_uid=uuid4(),
        title=faker.street_name(),
        author=faker.name(),
        publisher=faker.company(),
        category=faker.name(),
        admin_uid=uuid4(),
    )
