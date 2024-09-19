from unittest.mock import patch, AsyncMock

from fastapi import HTTPException, status
from root.app import app
import tests.utils as general_utils

from uuid import uuid4
from fastapi.testclient import TestClient
import json

TEST_CLIENT = TestClient(app=app)


@patch("routers.user_route.user_service")
async def test_sign_up_happy_path(mock_user_service):

    user = general_utils.get_user()
    user_uid = uuid4()
    user_profile = general_utils.get_user_profile(user=user, user_uid=user_uid)

    mock_user_service.user_sign_up = AsyncMock(return_value=user_profile.model_dump())

    response = TEST_CLIENT.post(url="/v1/user/sign-up", json=user.model_dump())
    response_json = response.json()
    assert response.status_code == 201
    assert response_json == json.loads(user_profile.model_dump_json())

    mock_user_service.user_sign_up.assert_awaited_once_with(user=user)


@patch("routers.user_route.user_service")
async def test_sign_up_sad_path(mock_user_service):

    user = general_utils.get_user()

    mock_user_service.user_sign_up.side_effect = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="user exists"
    )

    response = TEST_CLIENT.post(url="/v1/user/sign-up", json=user.model_dump())
    response_json = response.json()
    assert response.status_code == 400
    assert response_json == {"detail": "user exists"}


@patch("routers.user_route.user_service")
async def test_get_user_happy_path(mock_user_service):

    user = general_utils.get_user()
    user_uid = uuid4()
    user_profile = general_utils.get_user_profile(user=user, user_uid=user_uid)

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
async def test_get_user_via_mail_happy_path(mock_user_service):

    user = general_utils.get_user()
    user_uid = uuid4()
    user_profile = general_utils.get_user_profile(user=user, user_uid=user_uid)

    mock_user_service.get_user_by_mail = AsyncMock(
        return_value=user_profile.model_dump()
    )

    response = TEST_CLIENT.post(url="/v1/user/", json={"email": user.email})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == json.loads(user_profile.model_dump_json())

    mock_user_service.get_user_by_mail.assert_awaited_once_with(email=user.email)


@patch("routers.user_route.user_service")
async def test_get_user_via_mail_sad_path(mock_user_service):

    user = general_utils.get_user()

    mock_user_service.get_user_by_mail.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
    )

    response = TEST_CLIENT.post(url="/v1/user/", json={"email": user.email})
    response_json = response.json()
    assert response.status_code == 404
    assert response_json == {"detail": "user not found"}
