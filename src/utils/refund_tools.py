import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from utils.refund_mock_data import USERS, ORDERS, REFUNDS, REFUND_POLICIES


def get_user_orders(
    user_id: Optional[str] = None, email: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieve all orders for a specific user."""
    user = None
    
    if user_id:
        user = USERS.get(user_id)
    elif email:
        user = next((u for u in USERS.values() if u["email"] == email), None)
    
    if not user:
        return {
            "status": "not_found",
            "message": "User not found with the provided credentials",
            "requested": {"user_id": user_id, "email": email},
        }
    
    user_orders = [o for o in ORDERS if o["user_id"] == user["user_id"]]
    
    return {
        "status": "success",
        "user": {
            "user_id": user["user_id"],
            "name": user["name"],
            "membership_tier": user["membership_tier"],
        },
        "orders": user_orders,
        "total_orders": len(user_orders),
    }


def get_order_details(order_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific order."""
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    
    if not order:
        return {
            "status": "not_found",
            "message": f"Order {order_id} not found",
        }
    
    user = USERS.get(order["user_id"], {})
    
    return {
        "status": "success",
        "order": order,
        "customer": {
            "name": user.get("name"),
            "email": user.get("email"),
            "membership_tier": user.get("membership_tier"),
        },
    }


def check_refund_eligibility(order_id: str) -> Dict[str, Any]:
    """Check if an order is eligible for a refund."""
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    
    if not order:
        return {
            "status": "not_found",
            "eligible": False,
            "message": f"Order {order_id} not found",
        }
    
    user = USERS.get(order["user_id"], {})
    membership = user.get("membership_tier", "standard")
    
    return_window = REFUND_POLICIES.get(f"{membership}_return_window_days", 30)
    
    order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
    days_since_order = (datetime.now() - order_date).days
    
    reasons = []
    eligible = True
    
    if order["status"] not in ["delivered", "shipped"]:
        eligible = False
        reasons.append(f"Order status '{order['status']}' is not eligible for refund")
    
    if days_since_order > return_window:
        eligible = False
        reasons.append(f"Order is {days_since_order} days old, exceeds {return_window}-day return window")
    
    if not order.get("refund_eligible", True):
        eligible = False
        reasons.append("This order has been marked as non-refundable")
    
    existing_refund = next((r for r in REFUNDS if r["order_id"] == order_id), None)
    if existing_refund:
        eligible = False
        reasons.append(f"A refund request already exists for this order (Refund ID: {existing_refund['refund_id']})")
    
    return {
        "status": "success",
        "order_id": order_id,
        "eligible": eligible,
        "days_since_order": days_since_order,
        "return_window_days": return_window,
        "membership_tier": membership,
        "reasons": reasons if not eligible else ["Order is eligible for refund"],
        "refund_amount": order["price_usd"] * order["quantity"] if eligible else 0,
    }


def process_refund(
    order_id: str,
    reason: str,
    additional_notes: Optional[str] = None
) -> Dict[str, Any]:
    """Process a refund request for an eligible order."""
    eligibility = check_refund_eligibility(order_id)
    
    if not eligibility.get("eligible", False):
        return {
            "status": "rejected",
            "order_id": order_id,
            "message": "Refund request rejected",
            "reasons": eligibility.get("reasons", ["Order not eligible for refund"]),
        }
    
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        return {
            "status": "error",
            "message": f"Order {order_id} not found",
        }
    
    refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
    refund_amount = order["price_usd"] * order["quantity"]
    
    refund_record = {
        "refund_id": refund_id,
        "order_id": order_id,
        "user_id": order["user_id"],
        "amount_usd": refund_amount,
        "reason": reason,
        "additional_notes": additional_notes,
        "status": "approved",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimated_completion": f"{REFUND_POLICIES['processing_time_days']} business days",
        "payment_method": order["payment_method"],
    }
    
    REFUNDS.append(refund_record)
    
    return {
        "status": "approved",
        "refund_id": refund_id,
        "order_id": order_id,
        "refund_amount_usd": refund_amount,
        "reason": reason,
        "message": f"Refund approved. ${refund_amount:.2f} will be credited to your {order['payment_method']} within {REFUND_POLICIES['processing_time_days']} business days.",
        "estimated_completion": f"{REFUND_POLICIES['processing_time_days']} business days",
    }


def get_refund_status(
    refund_id: Optional[str] = None,
    order_id: Optional[str] = None
) -> Dict[str, Any]:
    """Check the status of an existing refund request."""
    refund = None
    
    if refund_id:
        refund = next((r for r in REFUNDS if r["refund_id"] == refund_id), None)
    elif order_id:
        refund = next((r for r in REFUNDS if r["order_id"] == order_id), None)
    
    if not refund:
        return {
            "status": "not_found",
            "message": "No refund request found with the provided ID",
            "requested": {"refund_id": refund_id, "order_id": order_id},
        }
    
    return {
        "status": "success",
        "refund": refund,
    }


def get_refund_policy() -> Dict[str, Any]:
    """Get information about the refund policy."""
    return {
        "status": "success",
        "policy": {
            "standard_return_window": f"{REFUND_POLICIES['standard_return_window_days']} days",
            "silver_member_return_window": f"{REFUND_POLICIES['silver_return_window_days']} days",
            "gold_member_return_window": f"{REFUND_POLICIES['gold_return_window_days']} days",
            "processing_time": f"{REFUND_POLICIES['processing_time_days']} business days",
            "eligible_reasons": REFUND_POLICIES["refund_reasons"],
            "notes": [
                "Items must be in original condition for full refund",
                "Refunds are processed to the original payment method",
                "Gold and Silver members enjoy extended return windows",
            ],
        },
    }


TOOL_REGISTRY: Dict[str, callable] = {
    "get_user_orders": get_user_orders,
    "get_order_details": get_order_details,
    "check_refund_eligibility": check_refund_eligibility,
    "process_refund": process_refund,
    "get_refund_status": get_refund_status,
    "get_refund_policy": get_refund_policy,
}
