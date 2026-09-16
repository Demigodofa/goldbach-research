import unittest

from tools.build_mobius_moment_square_critical_margin_sensitivity_audit import (
    build_receipt,
    polynomial_minimum,
)


class MobiusMomentSquareCriticalMarginSensitivityAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_minimum_helper_finds_quadratic_minimum(self):
        (value, parameter), _ = polynomial_minimum([5.0, -4.0, 2.0])
        self.assertAlmostEqual(float(value), 3.0)
        self.assertAlmostEqual(float(parameter), 1.0)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "MEASURE_critical_margin_coefficient_sensitivity")
        self.assertTrue(
            self.receipt["finite_coefficient_sensitivity_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["critical_margin_sensitivity_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_m167_is_weakest_provenance_margin(self):
        weakest = self.receipt["weakest_provenance_margin_row"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertLess(
            float(weakest["provenance_slack_above_tight_margin_decimal"]), 0)
        self.assertGreater(
            float(weakest["provenance_slack_above_robust_margin_decimal"]),
            0.006)

    def test_m167_loss_is_degree_five_coefficient_delta(self):
        row = self.receipt["weakest_provenance_margin_row"]
        self.assertEqual(row["nonzero_coefficient_delta_count"], 1)
        self.assertEqual(row["dominant_abs_contribution_degree"], 5)
        self.assertAlmostEqual(
            row["dominant_abs_contribution_over_direct_abs"], 1.0)
        contribution = row["nonzero_degree_contributions"][0]
        self.assertEqual(contribution["degree"], 5)
        self.assertEqual(contribution["coefficient_delta_decimal"], "-0.02000000000000000000000000000000000000000")
        self.assertLess(
            abs(float(row["minimizer_movement_delta_decimal"])), 1e-10)

    def test_largest_loss_matches_m167(self):
        largest_loss = self.receipt["largest_provenance_below_source_loss_row"]
        self.assertEqual(largest_loss["scale_modulus"], 167)
        self.assertLess(
            float(largest_loss[
                "total_provenance_minus_source_margin_delta_decimal"]),
            -2e-5)


if __name__ == "__main__":
    unittest.main()
