from services.book_service import update_book
import json
from schemas.book_schemas import BookUpdate


async def action_update_book(data: str):

    book_dict = json.loads(data)

    book = BookUpdate(**book_dict)
    try:
        await update_book(book_update=book, book_uid=book.book_uid)
    except Exception:
        pass
