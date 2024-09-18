from sqlalchemy.dialects.postgresql import UUID
from root.utils.abstract_base import AbstractBase

from sqlalchemy import String, Column, Date, Boolean, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from uuid import uuid4
from database.orms.user_orm import User


class Book(AbstractBase):
    __tablename__ = "book"
    book_uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    admin_uid = Column(UUID(as_uuid=True), index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    category = Column(String, nullable=True)
    is_borrowed = Column(Boolean, nullable=True, server_default=str(False))
    borrowed = relationship("BookBorrowed", back_populates="book")


class BookBorrowed(AbstractBase):
    __tablename__ = "book_borrowed"
    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    book_uid = Column(
        UUID(as_uuid=True),
        ForeignKey("book.book_uid", ondelete="CASCADE"),
    )
    borrowed_by = Column(
        UUID(as_uuid=True),
        ForeignKey("user.user_uid", ondelete="CASCADE"),
    )
    date_borrowed = Column(Date, nullable=True)
    duration_borrowed_for = Column(Integer, nullable=True)
    book = relationship("Book")
    borrower = relationship("User")
