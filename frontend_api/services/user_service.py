import logging
from schemas.user_schemas import User
import database.db_handlers.user_db_handler as user_db_handler
from fastapi import HTTPException, status
import services.mq_publisher as mq
from services.service_exception import NotFoundError
from uuid import UUID
import json


LOGGER = logging.getLogger(__name__)


async def get_user_by_mail(email: str):
    try:
        return await user_db_handler.get_user(email=email)
    except NotFoundError as e:
        raise e


# create record
async def user_sign_up(user: User):

    try:
        await get_user_by_mail(email=user.email)

        raise HTTPException(
            detail="user exists", status_code=status.HTTP_400_BAD_REQUEST
        )
    # else create record
    except NotFoundError:
        user_profile = await user_db_handler.create_user(user=user)

        # MQ publish

        data = json.dumps(user_profile.model_dump(), default=str)
        await mq.mq_publish(data=data, routing_key="create_library_user")  # noqa: F821
        return user_profile


# forget password
async def get_user(user_uid: UUID):

    try:

        return await user_db_handler.get_user_profile(user_uid=user_uid)
    except NotFoundError:
        raise HTTPException(
            detail="user is not found", status_code=status.HTTP_404_NOT_FOUND
        )

    ...
