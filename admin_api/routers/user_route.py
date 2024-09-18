from fastapi import APIRouter, Depends, status

import services.user_service as user_service
import schemas.user_schemas as schemas

from uuid import UUID

api_router = APIRouter(prefix="/v1/user", tags=["User Service"])


@api_router.get(
    "/{user_uid}", response_model=schemas.UserProfile, status_code=status.HTTP_200_OK
)
async def get_user(user_uid: UUID):
    return await user_service.get_user(user_uid=user_uid)


@api_router.get(
    "/", response_model=schemas.PaginatedUserProfile, status_code=status.HTTP_200_OK
)
async def get_users(
    user_filter: schemas.PaginatedQuery = Depends(schemas.PaginatedQuery),
):
    return await user_service.get_users()
