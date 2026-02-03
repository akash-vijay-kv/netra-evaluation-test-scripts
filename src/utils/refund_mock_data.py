from typing import Dict, Any, List
from datetime import datetime, timedelta

USERS: Dict[str, Dict[str, Any]] = {
    "U-001": {
        "user_id": "U-001",
        "name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-0101",
        "membership_tier": "gold",
    },
    "U-002": {
        "user_id": "U-002",
        "name": "Jane Doe",
        "email": "jane.doe@email.com",
        "phone": "+1-555-0102",
        "membership_tier": "silver",
    },
    "U-003": {
        "user_id": "U-003",
        "name": "Bob Wilson",
        "email": "bob.wilson@email.com",
        "phone": "+1-555-0103",
        "membership_tier": "standard",
    },
}

ORDERS: List[Dict[str, Any]] = [
    {
        "order_id": "ORD-1001",
        "user_id": "U-001",
        "product_name": "Wireless Bluetooth Headphones",
        "product_id": "PROD-101",
        "quantity": 1,
        "price_usd": 79.99,
        "order_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "status": "delivered",
        "payment_method": "credit_card",
        "refund_eligible": True,
    },
    {
        "order_id": "ORD-1002",
        "user_id": "U-001",
        "product_name": "USB-C Charging Cable",
        "product_id": "PROD-102",
        "quantity": 2,
        "price_usd": 15.99,
        "order_date": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
        "status": "delivered",
        "payment_method": "credit_card",
        "refund_eligible": False,
    },
    {
        "order_id": "ORD-1003",
        "user_id": "U-002",
        "product_name": "Mechanical Keyboard",
        "product_id": "PROD-103",
        "quantity": 1,
        "price_usd": 129.99,
        "order_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "status": "delivered",
        "payment_method": "paypal",
        "refund_eligible": True,
    },
    {
        "order_id": "ORD-1004",
        "user_id": "U-002",
        "product_name": "Laptop Stand",
        "product_id": "PROD-104",
        "quantity": 1,
        "price_usd": 49.99,
        "order_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "status": "shipped",
        "payment_method": "credit_card",
        "refund_eligible": True,
    },
    {
        "order_id": "ORD-1005",
        "user_id": "U-003",
        "product_name": "Wireless Mouse",
        "product_id": "PROD-105",
        "quantity": 1,
        "price_usd": 34.99,
        "order_date": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
        "status": "delivered",
        "payment_method": "debit_card",
        "refund_eligible": True,
    },
    {
        "order_id": "ORD-1006",
        "user_id": "U-003",
        "product_name": "Monitor Light Bar",
        "product_id": "PROD-106",
        "quantity": 1,
        "price_usd": 59.99,
        "order_date": (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
        "status": "delivered",
        "payment_method": "credit_card",
        "refund_eligible": False,
    },
]

REFUNDS: List[Dict[str, Any]] = []

REFUND_POLICIES: Dict[str, Any] = {
    "standard_return_window_days": 30,
    "gold_return_window_days": 60,
    "silver_return_window_days": 45,
    "processing_time_days": 5,
    "refund_reasons": [
        "defective_product",
        "wrong_item",
        "not_as_described",
        "changed_mind",
        "arrived_late",
        "damaged_in_shipping",
    ],
}
