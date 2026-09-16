import unittest

from tools.build_mobius_moment_square_sturm_margin_window_audit import (
    build_receipt,
    polynomial_minimum,
    root_count_for_shift,
)


class MobiusMomentSquareSturmMarginWindowAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_minimum_helper_finds_shifted_quartic_minimum(self):
        (value, parameter), _ = polynomial_minimum([3.0, -2.0, 1.0])
        self.assertAlmostEqual(float(value), 2.0)
        self.assertAlmostEqual(float(parameter), 1.0)

    def test_root_count_detects_margin_crossing(self):
        self.assertEqual(root_count_for_shift([1.0, 0.0, 1.0], 0), 0)
        self.assertEqual(root_count_for_shift([1.0, 0.0, 1.0], 2), 2)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "MEASURE_serialized_sturm_margin_window")
        self.assertTrue(
            self.receipt["finite_serialized_margin_window_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["critical_margin_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_m167_controls_source_and_provenance_margin_windows(self):
        source = self.receipt["weakest_source_curve_serialized_margin"]
        provenance = self.receipt["weakest_provenance_serialized_margin"]
        self.assertEqual(source["scale_modulus"], 167)
        self.assertEqual(provenance["scale_modulus"], 167)
        self.assertGreater(source["slack_above_tight_margin"], 0)
        self.assertLess(source["slack_above_tight_margin"], 2e-5)
        self.assertLess(provenance["slack_above_tight_margin"], 0)
        self.assertGreater(provenance["slack_above_tight_margin"], -2e-5)
        self.assertGreater(provenance["slack_above_robust_margin"], 0.006)

    def test_sturm_bracket_confirms_estimated_critical_margin(self):
        provenance = self.receipt["weakest_provenance_serialized_margin"]
        self.assertEqual(
            provenance["critical_margin_floor_1e6_rational"], "426981/1000000")
        self.assertEqual(
            provenance["critical_margin_floor_1e6_root_count"], 0)
        self.assertEqual(
            provenance["critical_margin_ceiling_1e6_rational"],
            "213491/500000")
        self.assertEqual(
            provenance["critical_margin_ceiling_1e6_root_count"], 2)

    def test_robust_margin_survives_both_serialized_families(self):
        self.assertTrue(
            self.receipt[
                "all_source_curve_serialized_root_free_at_robust_margin"])
        self.assertTrue(
            self.receipt[
                "all_provenance_serialized_root_free_at_robust_margin"])
        self.assertTrue(
            self.receipt[
                "all_source_curve_serialized_root_free_at_tight_margin"])
        self.assertFalse(
            self.receipt[
                "all_provenance_serialized_root_free_at_tight_margin"])


if __name__ == "__main__":
    unittest.main()
