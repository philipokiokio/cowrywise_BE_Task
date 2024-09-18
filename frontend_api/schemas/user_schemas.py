from root.utils.base_schemas import AbstractModel
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional


class User(AbstractModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserProfile(User):
    user_uid: UUID
    date_created_utc: datetime
    date_updated_utc: Optional[datetime] = None
