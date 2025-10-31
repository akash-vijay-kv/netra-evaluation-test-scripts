from typing import Dict, Any, List

SHELF: List[Dict[str, Any]] = [
    {
        "book_id": "B-001",
        "title": "Dune",
        "author": "Frank Herbert",
        "available": True,
        "price_usd": 14.99,
    },
    {
        "book_id": "B-002",
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available": True,
        "price_usd": 39.99,
    },
    {
        "book_id": "B-003",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "available": False,
        "price_usd": 34.95,
    },
]

BOOK_METADATA: Dict[str, Dict[str, Any]] = {
    "B-001": {
        "summary": "Epic science fiction saga about politics, ecology, and destiny on the desert planet Arrakis.",
        "pages": 688,
        "rating": 4.7,
        "genres": ["Science Fiction", "Classic"],
    },
    "B-002": {
        "summary": "Practical tips and philosophies for becoming a better, more pragmatic software developer.",
        "pages": 352,
        "rating": 4.8,
        "genres": ["Software", "Professional Development"],
    },
    "B-003": {
        "summary": "Guidelines and best practices for writing clean, maintainable code.",
        "pages": 464,
        "rating": 4.6,
        "genres": ["Software", "Best Practices"],
    },
}
