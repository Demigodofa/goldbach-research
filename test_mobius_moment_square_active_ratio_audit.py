import unittest

from tools.build_mobius_moment_square_active_ratio_audit import (
    build_receipt,
)


class MobiusMomentSquareActiveRatioAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "FALSIFY_moment_square_soft_direction_as_adverse_drag")
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["q286_reactivated"])
        self.assertFalse(
            self.receipt["mobius_covariance_theorem_proved"])
        self.assertFalse(
            self.receipt["uniform_active_full_lower_frame_proved"])

    def test_moment_square_curve_is_not_adverse_on_checked_scales(self):
        self.assertTrue(
            self.receipt[
                "all_moment_square_curve_ratios_above_one_half"])
        self.assertTrue(
            self.receipt["all_full_soft_ratios_above_one_half"])
        self.assertAlmostEqual(
            self.receipt["minimum_moment_square_active_over_full"],
            0.9441389892658896)
        self.assertAlmostEqual(
            self.receipt[
                "minimum_ratio_at_equilibrated_full_soft_parameter"],
            0.9122467414896579)

    def test_m167_soft_ratio_survives(self):
        rows = {
            row["scale_modulus"]: row
            for row in self.receipt["scale_results"]}
        self.assertAlmostEqual(
            rows[167]["moment_square_active_over_full_minimum"],
            0.9441389892658896)
        self.assertAlmostEqual(
            rows[167]["ratio_at_equilibrated_full_soft_parameter"],
            0.9193340666498803)
        self.assertAlmostEqual(
            rows[167]["equilibrated_full_soft_parameter"],
            0.2698106456761942)


if __name__ == "__main__":
    unittest.main()
