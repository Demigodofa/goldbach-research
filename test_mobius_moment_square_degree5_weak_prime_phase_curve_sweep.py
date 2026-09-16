import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_weak_prime_phase_curve_sweep import (
    active_row_start_sweep,
)


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-weak-prime-phase-curve-sweep.json")


class MobiusMomentSquareDegree5WeakPrimePhaseCurveSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_sweep_is_extended_local_row_start_band(self):
        self.assertEqual(active_row_start_sweep(), list(range(71)))
        self.assertEqual(self.receipt["scale_modulus"], 167)
        self.assertEqual(self.receipt["prime_modulus"], 181)
        self.assertEqual(self.receipt["row_count"], 35)
        self.assertEqual(self.receipt["ell_freeze"], 52)
        self.assertEqual(self.receipt["active_row_start_count"], 71)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_weak_prime_active_window_phase_curve")
        self.assertTrue(
            self.receipt["finite_weak_prime_phase_curve_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["phase_curve_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_all_swept_rows_dominate_one_half(self):
        self.assertEqual(self.receipt["component_row_count"], 213)
        self.assertEqual(self.receipt["degree5_total_row_count"], 71)
        self.assertEqual(self.receipt["dominance_row_count"], 284)
        self.assertEqual(self.receipt["failure_row_count"], 0)
        self.assertEqual(self.receipt["failure_rows"], [])
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 284, "zero": 0, "negative": 0})

    def test_each_label_summary_passes(self):
        self.assertEqual(
            set(self.receipt["label_summaries"]),
            {"00,12", "01,02", "01,11", "TOTAL"})
        for summary in self.receipt["label_summaries"].values():
            self.assertEqual(summary["row_count"], 71)
            self.assertTrue(
                summary["all_rows_dominate_one_half_signed_full"])
            self.assertEqual(
                summary["dominance_slack_sign_counts"],
                {"positive": 71, "zero": 0, "negative": 0})

    def test_weakest_phase_curve_row_is_recorded(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertEqual(weakest["prime_modulus"], 181)
        self.assertEqual(weakest["label"], "00,12")
        self.assertEqual(weakest["active_row_start"], 44)
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.5370450115638492)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.037045011563849206)


if __name__ == "__main__":
    unittest.main()
