from typing import List, Dict, Any

REFUND_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_user_orders",
            "description": "Retrieve all orders for a specific user by their user_id or email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique user identifier (e.g., U-001)",
                    },
                    "email": {
                        "type": "string",
                        "description": "The user's email address",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Get detailed information about a specific order by order_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique order identifier (e.g., ORD-1001)",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_refund_eligibility",
            "description": "Check if an order is eligible for a refund based on order status, date, and policies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique order identifier to check eligibility for",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Process a refund request for an eligible order. Returns refund confirmation or rejection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to process refund for",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for the refund request",
                        "enum": [
                            "defective_product",
                            "wrong_item",
                            "not_as_described",
                            "changed_mind",
                            "arrived_late",
                            "damaged_in_shipping",
                        ],
                    },
                    "additional_notes": {
                        "type": "string",
                        "description": "Any additional notes or comments from the customer",
                    },
                },
                "required": ["order_id", "reason"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_refund_status",
            "description": "Check the status of an existing refund request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "refund_id": {
                        "type": "string",
                        "description": "The refund request ID",
                    },
                    "order_id": {
                        "type": "string",
                        "description": "The original order ID",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_refund_policy",
            "description": "Get information about the refund policy including return windows and eligible reasons.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]
