from fastapi import APIRouter, Body, status
from pydantic import EmailStr

import services.user_service as user_service
import schemas.user_schemas as schemas

from uuid import UUID

api_router = APIRouter(prefix="/v1/user", tags=["User Service"])


@api_router.post(
    "/sign-up",
    response_model=schemas.UserProfile,
    status_code=status.HTTP_201_CREATED,
)
async def user_sign_up(user: schemas.User):
    return await user_service.user_sign_up(user=user)


@api_router.get(
    "/{user_uid}", response_model=schemas.UserProfile, status_code=status.HTTP_200_OK
)
async def get_user(user_uid: UUID):
    return await user_service.get_user(user_uid=user_uid)


@api_router.post(
    "/", response_model=schemas.UserProfile, status_code=status.HTTP_200_OK
)
async def get_user_via_mail(email: EmailStr = Body(embed=True)):
    return await user_service.get_user_by_mail(email=email)
