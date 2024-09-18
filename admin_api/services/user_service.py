import logging
from schemas.user_schemas import User
import database.db_handlers.user_db_handler as user_db_handler
from fastapi import HTTPException, status
from services.service_exception import NotFoundError
from uuid import UUID


LOGGER = logging.getLogger(__name__)


async def get_user_by_mail(email: str):
    try:
        return await user_db_handler.get_user(email=email)
    except NotFoundError as e:
        raise e


# create record
async def create_user(user: User):

    try:
        await get_user_by_mail(email=user.email)

        raise HTTPException(
            detail="user is exists", status_code=status.HTTP_400_BAD_REQUEST
        )
    # else create record
    except NotFoundError:
        user_profile = await user_db_handler.create_user(user=user)

        return user_profile


# forget password
async def get_user(user_uid: UUID):

    try:

        return await user_db_handler.get_user_profile(user_uid=user_uid)
    except NotFoundError:
        raise HTTPException(
            detail="user is not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_users(**kwargs):
    return await user_db_handler.get_users(**kwargs)
