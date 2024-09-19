from unittest.mock import patch, AsyncMock, Mock
import pytest
import json
from fastapi import HTTPException
from schemas.user_schemas import PaginatedUserProfile
from services.service_exception import NotFoundError
import tests.utils as general_utils
from uuid import uuid4
import services.user_service as user_service


@patch("services.user_service.user_db_handler")
async def test_get_user_by_mail_happy_path(mock_user_db):
    user_uid = uuid4()
    user = general_utils.get_user(user_uid=user_uid)
    user_profile = general_utils.get_user_profile(user=user)
    mock_user_db.get_user = AsyncMock(return_value=user_profile)

    await user_service.get_user_by_mail(email=user.email)
    mock_user_db.get_user.assert_called_with(email=user.email)


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_get_user_by_mail_sad_path(mock_user_db):

    user_uid = uuid4()
    user = general_utils.get_user(user_uid=user_uid)

    mock_user_db.get_user.side_effect = NotFoundError

    with pytest.raises(NotFoundError):

        await user_service.get_user_by_mail(email=user.email)


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_user_signup_sad_path(mock_user_db):
    user_uid = uuid4()
    user = general_utils.get_user(user_uid=user_uid)
    user_profile = general_utils.get_user_profile(user=user)

    mock_user_db.get_user.return_value = user_profile

    with pytest.raises(HTTPException):
        await user_service.create_user(user=user)

    ...


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_user_sign_up_happy_path(mock_user_db):

    user_uid = uuid4()
    user = general_utils.get_user(user_uid=user_uid)
    user_profile = general_utils.get_user_profile(user=user)

    mock_user_db.create_user.return_value = user_profile

    mock_user_db.get_user.side_effect = NotFoundError

    created_user_profile = await user_service.create_user(user=user)

    mock_user_db.get_user.assert_awaited_once_with(email=user.email)
    mock_user_db.create_user.assert_awaited_once_with(user=user)

    assert created_user_profile == user_profile


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_get_user_sad_path(mock_user_db):
    user_uid = uuid4()
    mock_user_db.get_user_profile.side_effect = NotFoundError

    with pytest.raises(HTTPException):
        await user_service.get_user(user_uid=user_uid)


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_get_user_happy_path(mock_user_db):
    user_uid = uuid4()
    user = general_utils.get_user(user_uid=user_uid)
    user_profile = general_utils.get_user_profile(user=user)

    mock_user_db.get_user_profile.return_value = user_profile

    fetched_user_profile = await user_service.get_user(user_uid=user_uid)

    mock_user_db.get_user_profile.assert_awaited_once_with(user_uid=user_uid)
    assert fetched_user_profile == user_profile


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_get_users_sad_path(mock_user_db):
    mock_user_db.get_users.return_value = PaginatedUserProfile()

    user_profiles = await user_service.get_users()

    assert user_profiles.result_set == []
    assert user_profiles.result_size == 0

    mock_user_db.get_users.assert_awaited_once_with()


@patch("services.user_service.user_db_handler", new_callable=AsyncMock)
async def test_get_users_happy_path(mock_user_db):
    user_profiles = []
    for i in range(5):
        user_uid = uuid4()
        user = general_utils.get_user(user_uid=user_uid)
        user_profiles.append(general_utils.get_user_profile(user=user))

    mock_user_db.get_users.return_value = PaginatedUserProfile(
        result_size=len(user_profiles), result_set=user_profiles
    )

    fetched_user_profiles = await user_service.get_users()

    assert fetched_user_profiles.result_size == len(user_profiles)

    mock_user_db.get_users.assert_awaited_once_with()
