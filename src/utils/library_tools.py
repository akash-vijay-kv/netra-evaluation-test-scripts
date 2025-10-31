import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from netra import Netra
from netra.session_manager import ConversationType
from netra.decorators import task

from utils.library_mock_data import SHELF, BOOK_METADATA


@task(name="fetch_current_shelf_books")
async def fetch_current_shelf_books() -> List[Dict[str, Any]]:
    shelf = SHELF
    Netra.add_conversation(
        conversation_type=ConversationType.OUTPUT,
        role="Tool",
        content=f"fetch_current_shelf_books_result: {shelf}",
    )
    return shelf


@task(name="order_book")
async def order_book(
    book_id: Optional[str] = None, title: Optional[str] = None, quantity: int = 1
) -> Dict[str, Any]:
    shelf = SHELF

    def match(b: Dict[str, Any]) -> bool:
        by_id = book_id and b.get("book_id") == book_id
        by_title = title and b.get("title", "").strip().lower() == title.strip().lower()
        return bool(by_id or by_title)

    book = next((b for b in shelf if match(b)), None)

    now = datetime.now()
    if not book:
        result = {
            "status": "not_found",
            "requested": {"book_id": book_id, "title": title, "quantity": quantity},
            "timestamp": str(now),
        }
    else:
        if book.get("available", False):
            result = {
                "status": "confirmed",
                "order_id": str(uuid.uuid4()),
                "book": {"book_id": book["book_id"], "title": book["title"]},
                "quantity": quantity,
                "eta_days": 3,
                "total_usd": round(book.get("price_usd", 0.0) * max(1, quantity), 2),
                "timestamp": str(now),
            }
        else:
            result = {
                "status": "backorder",
                "order_id": str(uuid.uuid4()),
                "book": {"book_id": book["book_id"], "title": book["title"]},
                "quantity": quantity,
                "eta_days": 10,
                "timestamp": str(now),
            }

    Netra.add_conversation(
        conversation_type=ConversationType.OUTPUT,
        role="Tool",
        content=f"order_book_result: {result}",
    )
    return result


@task(name="get_book_info")
async def get_book_info(
    book_id: Optional[str] = None, title: Optional[str] = None
) -> Dict[str, Any]:
    shelf = SHELF

    def match(b: Dict[str, Any]) -> bool:
        by_id = book_id and b.get("book_id") == book_id
        by_title = title and b.get("title", "").strip().lower() == title.strip().lower()
        return bool(by_id or by_title)

    book = next((b for b in shelf if match(b)), None)

    if not book:
        result = {
            "status": "not_found",
            "requested": {"book_id": book_id, "title": title},
        }
    else:
        m = BOOK_METADATA.get(book["book_id"], {})
        result = {
            "status": "success",
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "available": book["available"],
            "price_usd": book.get("price_usd"),
            "info": m,
        }

    Netra.add_conversation(
        conversation_type=ConversationType.OUTPUT,
        role="Tool",
        content=f"get_book_info_result: {result}",
    )
    return result
