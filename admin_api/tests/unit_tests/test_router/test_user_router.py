from unittest.mock import patch, AsyncMock

from fastapi import HTTPException, status
from root.app import app
from schemas.user_schemas import PaginatedUserProfile
import tests.utils as general_utils

from uuid import uuid4
from fastapi.testclient import TestClient
import json

TEST_CLIENT = TestClient(app=app)


@patch("routers.user_route.user_service")
async def test_get_user_happy_path(mock_user_service):
    user_uid = uuid4()
    user = general_utils.get_user(user_uid=user_uid)

    user_profile = general_utils.get_user_profile(user=user)

    mock_user_service.get_user = AsyncMock(return_value=user_profile.model_dump())

    response = TEST_CLIENT.get(url=f"/v1/user/{user_uid}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(user_profile.model_dump_json())

    mock_user_service.get_user.assert_awaited_once_with(user_uid=user_uid)


@patch("routers.user_route.user_service")
async def test_get_user_sad_path(mock_user_service):

    user_uid = uuid4()

    mock_user_service.get_user.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="user is not found"
    )

    response = TEST_CLIENT.get(url=f"/v1/user/{user_uid}")
    response_json = response.json()
    assert response.status_code == 404
    assert response_json == {"detail": "user is not found"}


@patch("routers.user_route.user_service")
async def test_get_users_happy_path(mock_user_service):
    user_profiles = []
    for i in range(5):
        user_uid = uuid4()
        user = general_utils.get_user(user_uid=user_uid)
        user_profiles.append(general_utils.get_user_profile(user=user))
    paginated_user_profile = PaginatedUserProfile(
        result_size=len(user_profiles), result_set=user_profiles
    )
    mock_user_service.get_users = AsyncMock(
        return_value=paginated_user_profile.model_dump()
    )

    response = TEST_CLIENT.get(url="/v1/user/")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(paginated_user_profile.model_dump_json())


@patch("routers.user_route.user_service")
async def test_get_users_sad_path(mock_user_service):

    paginated_user_profile = PaginatedUserProfile()
    mock_user_service.get_users = AsyncMock(
        return_value=paginated_user_profile.model_dump()
    )

    response = TEST_CLIENT.get(url="/v1/user/")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(paginated_user_profile.model_dump_json())
