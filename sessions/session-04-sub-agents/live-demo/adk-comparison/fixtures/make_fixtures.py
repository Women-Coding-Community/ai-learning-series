"""Generate the ShipIt fixtures deterministically. No network, no clock.

Run from adk-comparison/:  python3 fixtures/make_fixtures.py

Writes:
  fixtures/shipit/app/payments.py       two planted security issues
  fixtures/shipit/README.md             two planted docs drifts
  fixtures/shipit/tests/output.log      ~1,500 noisy lines, 2 real failures
  fixtures/shipit/tests/test_payments.py  small passing suite (for python3 -m unittest)
  fixtures/expected.json                ground truth for compare.py

expected.json lives OUTSIDE shipit/ on purpose: a coding agent opened inside
shipit/ must not be able to read the answers.
"""
import json
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).parent
SEED = 42

PAYMENTS_PY = '''"""ShipIt payments: take a card payment and look up past orders.

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
'''

README_MD = '''# ShipIt Payments

A tiny payments module for the ShipIt checkout.

## Endpoint

`POST /pay` takes JSON:

| Field      | Type   | Notes                                  |
|------------|--------|----------------------------------------|
| `amount`   | number | Amount in pounds, for example `19.99`  |
| `currency` | string | `GBP`, `EUR` or `USD`                  |
| `token`    | string | Card token from the front end          |

Failed charges are retried. `retries` defaults to 5.

## Configuration

`SECRET_KEY` is read from the payments module.

## Running tests

```
python3 -m unittest -v
```

Test output is written to `tests/output.log`.
'''

TEST_PAYMENTS_PY = '''import unittest

from app import payments


class PaymentTests(unittest.TestCase):
    def test_take_payment_gbp(self):
        self.assertEqual(payments.take_payment(1999, "GBP", "tok_1")["status"], "ok")

    def test_unsupported_currency(self):
        with self.assertRaises(ValueError):
            payments.take_payment(1999, "JPY", "tok_1")

    def test_zero_amount_rejected(self):
        with self.assertRaises(ValueError):
            payments.take_payment(0, "GBP", "tok_1")


if __name__ == "__main__":
    unittest.main()
'''

MODULES = ["checkout", "cart", "shipping", "auth", "search", "inventory", "email", "tax", "coupons"]
PASSING = [
    "test_cart_add_item", "test_cart_remove_item", "test_login_ok", "test_login_bad_password",
    "test_shipping_rate_uk", "test_shipping_rate_eu", "test_tax_vat_standard", "test_coupon_percent",
    "test_coupon_expired", "test_search_prefix", "test_stock_reserve", "test_email_template",
    "test_refund_full", "test_refund_partial_even", "test_webhook_signature", "test_webhook_ok",
    "test_checkout_total", "test_order_history", "test_currency_format", "test_address_validation",
]

FAILURE_ROUNDING = [
    "tests/test_refunds.py::test_refund_rounding FAILED",
    "________________________ test_refund_rounding ________________________",
    "",
    "    def test_refund_rounding():",
    "        refund = calculate_refund(amount_pence=1999, percent=50)",
    ">       assert refund == 1000",
    "E       assert 999 == 1000",
    "E        +  where 999 = calculate_refund(amount_pence=1999, percent=50)",
    "",
    "tests/test_refunds.py:42: AssertionError",
]
FAILURE_TIMEOUT = [
    "tests/test_webhooks.py::test_webhook_retry FAILED",
    "________________________ test_webhook_retry ________________________",
    "",
    "    def test_webhook_retry():",
    "        result = deliver_webhook(url, payload, retries=3)",
    ">       assert result.delivered",
    "E       TimeoutError: webhook did not respond within 5.0s (attempt 3 of 3)",
    "",
    "tests/test_webhooks.py:77: TimeoutError",
]


def build_log(rng: random.Random) -> str:
    """Build a noisy test log with exactly two real failures at seeded positions."""
    seconds = 0

    def ts() -> str:
        nonlocal seconds
        seconds += rng.randint(0, 3)
        return f"2026-10-20T09:{(seconds // 60) % 60:02d}:{seconds % 60:02d}.{rng.randint(0, 999):03d}Z"

    noise = []
    passed = 0
    while len(noise) < 1470:
        module = rng.choice(MODULES)
        roll = rng.random()
        if roll < 0.40:
            noise.append(f"{ts()} DEBUG [{module}] cache lookup key={rng.randint(1000, 99999)} hit={rng.choice(['true', 'false'])}")
        elif roll < 0.60:
            noise.append(f"{ts()} INFO  [{module}] request {rng.randint(100000, 999999)} completed in {rng.randint(3, 480)}ms")
        elif roll < 0.70:
            noise.append(f"{ts()} WARN  [db] connection pool at {rng.choice([70, 80, 90])}% capacity")
        elif roll < 0.78:
            noise.append(f"{ts()} WARN  [{module}] DeprecationWarning: datetime.utcnow() is deprecated, use datetime.now(datetime.UTC)")
        else:
            name = rng.choice(PASSING)
            noise.append(f"tests/test_{module}.py::{name} PASSED")
            passed += 1

    first = rng.randint(200, 600)
    second = rng.randint(900, 1300)
    lines = noise[:first] + FAILURE_ROUNDING + noise[first:second] + FAILURE_TIMEOUT + noise[second:]
    header = [
        "============================= test session starts ==============================",
        "platform linux -- Python 3.13.1, pytest-8.3.2",
        f"collected {passed + 2} items",
        "",
    ]
    footer = [
        "",
        "=========================== short test summary info ============================",
        "FAILED tests/test_refunds.py::test_refund_rounding - assert 999 == 1000",
        "FAILED tests/test_webhooks.py::test_webhook_retry - TimeoutError: webhook did not respond within 5.0s",
        f"================== 2 failed, {passed} passed, 4 warnings in 41.07s ==================",
    ]
    return "\n".join(header + lines + footer) + "\n"


def expected_findings() -> list:
    """Ground truth. A finding counts as found when min_match keywords appear in the report.

    A keyword starting with 're:' is a case-insensitive regular expression.
    'evidence' is a string that must appear in 'file'; the tests check it.
    """
    return [
        {"id": "sec-hardcoded-secret", "category": "security", "file": "app/payments.py",
         "keywords": ["sk_test_FAKE_DO_NOT_USE", "hardcoded", "secret"], "min_match": 2,
         "evidence": 'SECRET_KEY = "sk_test_FAKE_DO_NOT_USE"'},
        {"id": "sec-sql-injection", "category": "security", "file": "app/payments.py",
         "keywords": ["f-string", "sql injection", "parameteris"], "min_match": 2,
         "evidence": 'query = f"SELECT'},
        {"id": "test-refund-rounding", "category": "tests", "file": "tests/output.log",
         "keywords": ["test_refund_rounding", "rounding", "999"], "min_match": 2,
         "evidence": "test_refund_rounding FAILED"},
        {"id": "test-webhook-timeout", "category": "tests", "file": "tests/output.log",
         "keywords": ["test_webhook_retry", "timeout", "webhook"], "min_match": 2,
         "evidence": "test_webhook_retry FAILED"},
        {"id": "docs-amount-units", "category": "docs", "file": "README.md",
         "keywords": ["pounds", "amount_pence", "pence"], "min_match": 2,
         "evidence": "Amount in pounds"},
        {"id": "docs-retries-default", "category": "docs", "file": "README.md",
         "keywords": ["retries", "re:\\b5\\b", "re:\\b3\\b"], "min_match": 3,
         "evidence": "`retries` defaults to 5"},
    ]


def generate(root: pathlib.Path = HERE) -> None:
    """Write every fixture under root (shipit/ and expected.json)."""
    shipit = root / "shipit"
    files = {
        "app/__init__.py": "",
        "tests/__init__.py": "",
        "app/payments.py": PAYMENTS_PY,
        "README.md": README_MD,
        "tests/test_payments.py": TEST_PAYMENTS_PY,
        "tests/output.log": build_log(random.Random(SEED)),
    }
    for relative, content in files.items():
        target = shipit / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    (root / "expected.json").write_text(json.dumps(expected_findings(), indent=2) + "\n")


if __name__ == "__main__":
    generate()
    print(f"Fixtures written to {HERE}", file=sys.stderr)
