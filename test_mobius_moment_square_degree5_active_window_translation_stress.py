import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_active_window_translation_stress import (
    active_row_starts,
)


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-active-window-translation-stress.json")


class MobiusMomentSquareDegree5ActiveWindowTranslationStressTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_row_starts_translate_source_active_window(self):
        self.assertEqual(active_row_starts(), [33, 34, 35, 36, 37])
        self.assertEqual(self.receipt["scale_modulus"], 167)
        self.assertEqual(self.receipt["base_parameters"]["row_count"], 35)
        self.assertEqual(
            self.receipt["base_parameters"]["active_row_start"], 35)
        self.assertEqual(
            self.receipt["base_parameters"]["active_row_stop"], 70)
        self.assertEqual(
            self.receipt["active_row_starts"], [33, 34, 35, 36, 37])
        self.assertEqual(
            self.receipt["active_row_start_offsets"], [-2, -1, 0, 1, 2])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "STRESS_degree5_active_window_translation_dominance")
        self.assertTrue(
            self.receipt["finite_active_window_translation_stress_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["active_window_translation_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_all_translated_window_rows_dominate_one_half(self):
        self.assertEqual(self.receipt["window_count"], 5)
        self.assertEqual(self.receipt["prime_count_per_window"], 29)
        self.assertEqual(self.receipt["component_row_count"], 435)
        self.assertEqual(self.receipt["degree5_total_row_count"], 145)
        self.assertEqual(self.receipt["dominance_row_count"], 580)
        self.assertEqual(self.receipt["failure_row_count"], 0)
        self.assertEqual(self.receipt["failure_rows"], [])
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 580, "zero": 0, "negative": 0})

    def test_each_window_summary_passes(self):
        self.assertEqual(len(self.receipt["window_summaries"]), 5)
        for summary in self.receipt["window_summaries"]:
            self.assertEqual(summary["prime_count"], 29)
            self.assertEqual(summary["component_row_count"], 87)
            self.assertEqual(summary["degree5_total_row_count"], 29)
            self.assertEqual(summary["dominance_row_count"], 116)
            self.assertTrue(
                summary["all_rows_dominate_one_half_signed_full"])
            self.assertEqual(
                summary["dominance_slack_sign_counts"],
                {"positive": 116, "zero": 0, "negative": 0})

    def test_weakest_translated_window_row_is_recorded(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertEqual(weakest["active_row_start"], 36)
        self.assertEqual(weakest["prime_modulus"], 181)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.5490505738773274)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.049050573877327364)


if __name__ == "__main__":
    unittest.main()
