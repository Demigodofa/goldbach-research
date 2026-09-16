import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_p379_cross_scale_audit import (
    PRIME_MODULUS,
    SCALE_MODULI,
    scale_class,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-p379-cross-scale-audit.json")


class MobiusMomentSquareDegree5SourceStartP379CrossScaleAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_source_start_p379_cross_scale_stress")
        self.assertEqual(self.receipt["prime_modulus"], PRIME_MODULUS)
        self.assertTrue(self.receipt["finite_attention_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["p379_stress_theorem_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])

    def test_scale_selection_and_classes_are_explicit(self):
        self.assertEqual(self.receipt["scale_moduli"], list(SCALE_MODULI))
        self.assertEqual(scale_class(191), "original_checked_scale")
        self.assertEqual(scale_class(229), "fresh_full_sweep_scale")
        self.assertEqual(scale_class(293), "fresh_unswept_scale")
        for scale_row in self.receipt["scale_results"]:
            scale = scale_row["scale_modulus"]
            self.assertLessEqual(scale, PRIME_MODULUS)
            self.assertLessEqual(PRIME_MODULUS, 2 * scale)
            self.assertEqual(scale_row["prime_modulus"], PRIME_MODULUS)

    def test_all_p379_cross_scale_rows_pass(self):
        self.assertEqual(self.receipt["scale_count"], 9)
        self.assertEqual(self.receipt["component_row_count"], 27)
        self.assertEqual(self.receipt["degree5_total_row_count"], 9)
        self.assertEqual(self.receipt["dominance_row_count"], 36)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 36, "zero": 0, "negative": 0})

    def test_global_weakest_is_m229_component(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 229)
        self.assertEqual(weakest["prime_modulus"], 379)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9018909662403138)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.40189096624031384)

    def test_component_shift_is_recorded_at_high_scales(self):
        by_scale = {
            row["scale_modulus"]: row
            for row in self.receipt["weakest_scale_rows"]
        }
        self.assertEqual(by_scale[191]["weakest_label"], "00,12")
        self.assertEqual(by_scale[331]["weakest_label"], "00,12")
        self.assertEqual(by_scale[353]["weakest_label"], "01,02")
        self.assertEqual(by_scale[379]["weakest_label"], "01,02")


if __name__ == "__main__":
    unittest.main()
