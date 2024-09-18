from services.book_service import create_book
import json
from schemas.book_schemas import Book


async def action_create_book(data: str):

    book_dict = json.loads(data)
    print(book_dict)
    book = Book(**book_dict)
    try:
        await create_book(book=book)
    except Exception:
        pass
