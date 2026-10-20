# ShipIt Payments

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
