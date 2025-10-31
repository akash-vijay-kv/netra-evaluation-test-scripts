from typing import List, Dict, Any

LIBRARY_TOOLS_V1: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "fetch_current_shelf_books",
            "description": "Get the list of books currently on the user's shelf.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_book",
            "description": "Place an order for a book by book_id or title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "string"},
                    "title": {"type": "string"},
                    "quantity": {"type": "integer", "minimum": 1},
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_book_info",
            "description": "Get detailed information for a book by book_id or title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "string"},
                    "title": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
]


LIBRARY_TOOLS_V2: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "fetch_current_shelf_books",
            "description": "Get the list of books currently on the user's shelf.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_book_info",
            "description": "Get detailed information for a book by book_id or title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "string"},
                    "title": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
]