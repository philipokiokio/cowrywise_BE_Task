import uuid
import tests.utils as general_utils


import pytest

from database.db_handlers import user_db_handler
import tests.unit_tests.test_db_handlers.db_test_utils as seeder_db_handler
from services.service_exception import (
    NotFoundError,
    CreateError,
)


async def test_create_user_happy_path(session):

    user = general_utils.get_user()

    user_profile = await user_db_handler.create_user(user=user)
    assert user_profile.first_name == user.first_name
    assert user_profile.last_name == user.last_name
    assert user_profile.email == user.email


async def test_create_user_sad_path(session):
    user = general_utils.get_user()
    await seeder_db_handler.create_user(user=user)

    with pytest.raises(CreateError):
        await user_db_handler.create_user(user=user)


async def test_get_user_happy_path(session):
    user = general_utils.get_user()
    user_profile = await seeder_db_handler.create_user(user=user)

    fetched_user_profile = await user_db_handler.get_user(email=user.email)
    assert fetched_user_profile == user_profile


async def test_get_user_sad_path(session):
    user = general_utils.get_user()
    with pytest.raises(NotFoundError):
        await user_db_handler.get_user(email=user.email)


async def test_get_users_sad_path(session):

    with pytest.raises(NotFoundError):
        await user_db_handler.get_user_profile(user_uid=uuid.uuid4())


async def test_get_users_path_path(session):

    user = general_utils.get_user()
    user_profile = await seeder_db_handler.create_user(user=user)

    fetched_user_profile = await user_db_handler.get_user_profile(
        user_uid=user_profile.user_uid
    )

    assert user_profile == fetched_user_profile
