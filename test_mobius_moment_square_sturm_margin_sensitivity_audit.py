import unittest

from tools.build_mobius_moment_square_sturm_margin_sensitivity_audit import (
    build_receipt,
    root_count_for_coefficients,
)


class MobiusMomentSquareSturmMarginSensitivityAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_root_counter_detects_shift_failure(self):
        self.assertEqual(root_count_for_coefficients([1.0, 0.0, 1.0], 2), 2)
        self.assertEqual(root_count_for_coefficients([1.0, 0.0, 1.0], 0), 0)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "FALSIFY_tight_margin_from_serialized_provenance_coefficients")
        self.assertTrue(
            self.receipt["finite_serialization_sensitivity_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["tight_margin_serialized_provenance_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_tight_margin_fails_only_serialized_provenance_path(self):
        self.assertTrue(self.receipt["tight_source_curve_margin_passes"])
        self.assertFalse(
            self.receipt["tight_provenance_serialized_margin_passes"])
        tight = self.receipt["margin_results"][0]
        self.assertEqual(tight["margin_rational"], "427/1000")
        self.assertEqual(tight["failing_provenance_scales"], [167])
        rows = {
            row["scale_modulus"]: row for row in tight["rows"]}
        self.assertEqual(
            rows[167]["provenance_serialized_real_root_count"], 2)

    def test_conservative_margin_survives_both_serializations(self):
        self.assertTrue(self.receipt["robust_source_curve_margin_passes"])
        self.assertTrue(
            self.receipt["robust_provenance_serialized_margin_passes"])
        robust = self.receipt["margin_results"][1]
        self.assertEqual(robust["margin_rational"], "21/50")
        self.assertEqual(robust["failing_provenance_scales"], [])


if __name__ == "__main__":
    unittest.main()
