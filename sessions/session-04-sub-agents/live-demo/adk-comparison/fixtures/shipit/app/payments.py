"""ShipIt payments: take a card payment and look up past orders.

Flask-style handlers. In the real app Flask registers pay_endpoint at POST /pay.
"""
import sqlite3
import time

SECRET_KEY = "sk_test_FAKE_DO_NOT_USE"
DB_PATH = "shipit.db"
SUPPORTED_CURRENCIES = ("GBP", "EUR", "USD")


def get_db() -> sqlite3.Connection:
    """Open the orders database."""
    return sqlite3.connect(DB_PATH)


def find_orders(customer_email: str) -> list:
    """Return every order placed by this customer."""
    db = get_db()
    query = f"SELECT id, total_pence, currency FROM orders WHERE email = '{customer_email}'"
    rows = db.execute(query).fetchall()
    db.close()
    return rows


def charge_card(amount_pence: int, currency: str, token: str) -> dict:
    """Call the payment provider. Stubbed here so the demo needs no network."""
    if token.startswith("tok_bad"):
        raise ConnectionError("provider unavailable")
    return {"status": "ok", "amount_pence": amount_pence, "currency": currency}


def take_payment(amount_pence: int, currency: str, token: str, retries: int = 3) -> dict:
    """Charge a card, retrying on connection errors."""
    if amount_pence <= 0:
        raise ValueError("amount_pence must be positive")
    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"unsupported currency: {currency}")
    last_error = None
    for attempt in range(retries):
        try:
            return charge_card(amount_pence, currency, token)
        except ConnectionError as error:
            last_error = error
            time.sleep(0.1 * (attempt + 1))
    raise RuntimeError(f"payment failed after {retries} attempts") from last_error


def pay_endpoint(body: dict) -> tuple:
    """POST /pay handler. Returns (json body, HTTP status)."""
    try:
        result = take_payment(body["amount_pence"], body["currency"], body["token"])
    except (KeyError, ValueError) as error:
        return {"error": str(error)}, 400
    except RuntimeError as error:
        return {"error": str(error)}, 502
    return result, 200
