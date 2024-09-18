from sqlalchemy import String, Column
from root.utils.abstract_base import AbstractBase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4


class User(AbstractBase):
    __tablename__ = "user"
    user_uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    book_borrowed = relationship("BookBorrowed", back_populates="borrower")
