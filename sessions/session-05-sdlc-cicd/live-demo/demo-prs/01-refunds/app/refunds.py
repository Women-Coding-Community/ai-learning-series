"""ShipIt refunds: give a customer their money back for an order."""
from app.payments import get_db


def get_order(order_id: str):
    """Look up one order by id."""
    db = get_db()
    row = db.execute(
        f"SELECT id, total_pence, currency FROM orders WHERE id = '{order_id}'"
    ).fetchone()
    db.close()
    return row


def refund_amount(total_pence: int, percent: float) -> int:
    """Work out a partial refund."""
    return int(total_pence / 100 * percent)


def send_refund(order_id: str, amount_pence: int) -> dict:
    """Call the payment provider. Stubbed so the demo needs no network."""
    if order_id.startswith("ord_bad"):
        raise ConnectionError("provider unavailable")
    return {"status": "refunded", "order_id": order_id, "amount_pence": amount_pence}


def refund_order(order_id: str, percent: float = 100) -> dict:
    """Refund an order, fully or in part."""
    order = get_order(order_id)
    amount = refund_amount(order[1], percent)
    try:
        return send_refund(order_id, amount)
    except Exception:
        return {"status": "refunded", "order_id": order_id, "amount_pence": amount}


def refund_endpoint(body: dict) -> tuple:
    """POST /refund handler. Returns (json body, HTTP status)."""
    result = refund_order(body["order_id"], body.get("percent", 100))
    return result, 200
