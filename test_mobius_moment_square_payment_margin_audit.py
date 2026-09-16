import unittest

import numpy as np

from tools.build_mobius_moment_square_payment_margin_audit import (
    build_receipt,
    payment_row,
)


class MobiusMomentSquarePaymentMarginAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_payment_row_records_unnormalized_half_margin(self):
        active = np.diag((7.0, 1.0, 1.0, 1.0, 1.0, 1.0))
        full = np.diag((10.0, 1.0, 1.0, 1.0, 1.0, 1.0))
        row = payment_row("infinity", None, active, full)
        self.assertEqual(row["active_value"], 7.0)
        self.assertEqual(row["full_value"], 10.0)
        self.assertEqual(row["half_frame_margin"], 2.0)
        self.assertEqual(row["half_frame_margin_over_full"], 0.2)
        self.assertEqual(row["active_minus_full"], -3.0)
        self.assertTrue(row["half_frame_margin_positive"])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "TARGET_moment_square_half_frame_payment_margin")
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["q286_reactivated"])
        self.assertFalse(
            self.receipt[
                "moment_square_half_frame_payment_theorem_proved"])
        self.assertFalse(
            self.receipt["uniform_active_full_lower_frame_proved"])

    def test_checked_directions_have_positive_half_frame_margin(self):
        self.assertEqual(self.receipt["direction_count"], 12)
        self.assertTrue(self.receipt["all_half_frame_margins_positive"])
        self.assertAlmostEqual(
            self.receipt["minimum_half_frame_margin_over_full"],
            0.4122467414896579)
        weakest = self.receipt["weakest_half_frame_margin_ratio_row"]
        self.assertEqual(weakest["scale_modulus"], 127)
        self.assertEqual(
            weakest["direction"],
            "diagonal_equilibrated_full_soft_parameter")
        self.assertAlmostEqual(
            weakest["half_frame_margin"], 0.9836755290161818)

    def test_active_does_not_always_exceed_full(self):
        row = self.receipt["most_negative_active_minus_full_row"]
        self.assertEqual(row["scale_modulus"], 127)
        self.assertEqual(
            row["direction"],
            "diagonal_equilibrated_full_soft_parameter")
        self.assertAlmostEqual(
            row["active_minus_full_over_full"],
            -0.0877532585103421)
        self.assertGreater(row["half_frame_margin"], 0.0)


if __name__ == "__main__":
    unittest.main()
