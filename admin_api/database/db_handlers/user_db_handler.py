from database.orms.user_orm import User as User_DB
from database.orms.book_orm import BookBorrowed as BorrowedBook_DB

from root.database import async_session
import logging
from schemas.user_schemas import (
    User,
    UserProfile,
    PaginatedUserProfile,
    BorrowBookProfile,
)
from sqlalchemy import insert, select
from services.service_exception import (
    CreateError,
    NotFoundError,
)
from uuid import UUID
from sqlalchemy.orm import joinedload

LOGGER = logging.getLogger(__name__)


async def create_user(user: User) -> UserProfile:
    async with async_session() as session:
        stmt = insert(User_DB).values(user.model_dump()).returning(User_DB)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if not result:
            LOGGER.error("create_user failed")
            session.rollback()
            raise CreateError

        await session.commit()
        return UserProfile(**result.as_dict())


async def get_user(email: str):
    async with async_session() as session:
        result = (
            await session.execute(select(User_DB).where(User_DB.email == email))
        ).scalar_one_or_none()

        if not result:
            raise NotFoundError

        return UserProfile(**result.as_dict())


async def get_user_profile(user_uid: UUID):
    async with async_session() as session:
        result = (
            (
                await session.execute(
                    select(User_DB)
                    .options(
                        joinedload(User_DB.book_borrowed).joinedload(
                            BorrowedBook_DB.book
                        )
                    )
                    .where(User_DB.user_uid == user_uid)
                )
            )
            .unique()
            .scalar_one_or_none()
        )

        if not result:
            raise NotFoundError

        return UserProfile(
            **result.as_dict(),
            borrowed_record=[
                BorrowBookProfile(**borrowed.as_dict(), book=borrowed.book)
                for borrowed in result.book_borrowed
            ]
        )


async def get_users(**kwargs):

    limit = kwargs.get("limit", 50)
    offset = kwargs.get("offset", 0)

    async with async_session() as session:

        stmt = (
            select(User_DB)
            .options(joinedload(User_DB.book_borrowed).joinedload(BorrowedBook_DB.book))
            .limit(limit=limit)
            .offset(offset=offset)
        )

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        if not result:

            return PaginatedUserProfile()

        return PaginatedUserProfile(
            result_set=[
                UserProfile(
                    **x.as_dict(),
                    borrowed_record=[
                        BorrowBookProfile(**borrowed.as_dict(), book=borrowed.book)
                        for borrowed in x.book_borrowed
                    ]
                )
                for x in result
            ],
            result_size=len(result),
        )
