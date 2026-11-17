import unittest

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
