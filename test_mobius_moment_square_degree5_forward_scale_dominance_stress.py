import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-adjacent-scale-dominance-stress.json")


class MobiusMomentSquareDegree5ForwardScaleDominanceStressTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "STRESS_degree5_forward_scale_primewise_dominance")
        self.assertTrue(
            self.receipt["finite_forward_scale_dominance_stress_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["forward_scale_dominance_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_adjacent_scale_rows_dominate_one_half(self):
        self.assertEqual(self.receipt["scales"], [229])
        self.assertEqual(self.receipt["prime_count_total"], 39)
        self.assertEqual(self.receipt["component_row_count"], 117)
        self.assertEqual(self.receipt["degree5_total_row_count"], 39)
        self.assertEqual(self.receipt["dominance_row_count"], 156)
        self.assertEqual(self.receipt["failure_row_count"], 0)
        self.assertEqual(self.receipt["failure_rows"], [])
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 156, "zero": 0, "negative": 0})

    def test_weakest_forward_row_is_recorded(self):
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

    def test_scale_summary_matches_global_result(self):
        self.assertEqual(len(self.receipt["scale_summaries"]), 1)
        summary = self.receipt["scale_summaries"][0]
        self.assertEqual(summary["scale_modulus"], 229)
        self.assertEqual(
            summary["minimum_dominance_slack_above_one_half"],
            self.receipt["minimum_dominance_slack_above_one_half"])
        self.assertEqual(
            summary["dominance_slack_sign_counts"],
            self.receipt["all_dominance_slack_sign_counts"])


if __name__ == "__main__":
    unittest.main()
