import unittest

from app import refunds


class RefundTests(unittest.TestCase):
    def test_full_refund_amount(self):
        self.assertEqual(refunds.refund_amount(2000, 100), 2000)

    def test_half_refund_amount(self):
        self.assertEqual(refunds.refund_amount(2000, 50), 1000)

    def test_send_refund(self):
        self.assertEqual(refunds.send_refund("ord_1", 500)["status"], "refunded")


if __name__ == "__main__":
    unittest.main()
