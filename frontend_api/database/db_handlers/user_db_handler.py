from database.orms.user_orm import User as User_DB
from root.database import async_session
import logging
from schemas.user_schemas import (
    User,
    UserProfile,
)
from sqlalchemy import insert, select
from services.service_exception import (
    CreateError,
    NotFoundError,
)
from sqlalchemy.exc import IntegrityError

from uuid import UUID


LOGGER = logging.getLogger(__name__)


async def create_user(user: User) -> UserProfile:
    async with async_session() as session:
        stmt = insert(User_DB).values(user.model_dump()).returning(User_DB)
        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()

            if not result:
                LOGGER.error("create_user failed")
                await session.rollback()
                raise CreateError

        except IntegrityError:
            await session.rollback()
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
            await session.execute(select(User_DB).where(User_DB.user_uid == user_uid))
        ).scalar_one_or_none()

        if not result:
            raise NotFoundError

        return UserProfile(**result.as_dict())
