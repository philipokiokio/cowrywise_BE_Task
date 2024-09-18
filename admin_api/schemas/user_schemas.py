from root.utils.base_schemas import AbstractModel, PaginatedQuery
from pydantic import EmailStr, conint
from datetime import datetime
from uuid import UUID
from typing import Optional

from schemas.book_schemas import BorrowBookProfile


class User(AbstractModel):
    user_uid: UUID
    first_name: str
    last_name: str
    email: EmailStr


class UserProfile(User):
    date_created_utc: datetime
    date_updated_utc: Optional[datetime] = None
    borrowed_record: list[BorrowBookProfile] = []


class PaginatedUserProfile(AbstractModel):
    result_set: list[UserProfile] = []
    result_size: conint(ge=0) = 0
