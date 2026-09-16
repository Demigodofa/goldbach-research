import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-far-tail-subband-balance-audit.json")


class MobiusMomentSquareDegree5Q46189FarTailSubbandBalanceTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_far_tail_subband_balance")
        self.assertTrue(
            self.receipt["finite_far_tail_subband_balance_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["far_band_positive_share_theorem_proved"])
        self.assertFalse(self.receipt["far_band_pressure_theorem_proved"])
        self.assertFalse(self.receipt["tail_band_pressure_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_far_band_positive_share_and_total_separate(self):
        summary = self.receipt["separation_summary"]
        self.assertAlmostEqual(
            summary["adverse_far_positive_fraction"],
            0.4408502583196725,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_replacement_far_positive_fraction"],
            0.46558306565994817,
            places=15)
        self.assertEqual(
            summary["minimum_replacement_far_positive_fraction_denominator"],
            62985)
        self.assertAlmostEqual(
            summary["far_positive_fraction_gap"],
            0.024732807340275664,
            places=15)
        self.assertAlmostEqual(
            summary["adverse_far_total_over_diagonal"],
            -0.47656170489466876,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_replacement_far_total_over_diagonal"],
            -0.2285960671576456,
            places=15)
        self.assertTrue(
            self.receipt["classification"][
                "far_positive_share_separates_finite_family"])
        self.assertTrue(
            self.receipt["classification"][
                "far_total_pressure_separates_finite_family"])

    def test_tail_band_is_not_the_separator(self):
        tail = self.receipt["tail_non_separator"]
        self.assertFalse(tail["tail_positive_fraction_separates"])
        self.assertFalse(tail["tail_total_separates"])
        self.assertEqual(
            tail["minimum_replacement_tail_positive_fraction_denominator"],
            40755)
        self.assertEqual(
            tail["minimum_replacement_tail_total_denominator"],
            40755)
        self.assertLess(
            tail["minimum_replacement_tail_positive_fraction"],
            tail["adverse_tail_positive_fraction"])
        self.assertLess(
            tail["minimum_replacement_tail_total_over_diagonal"],
            tail["adverse_tail_total_over_diagonal"])

    def test_next_action_targets_far_band(self):
        candidate = self.receipt["candidate_next_action"]
        self.assertEqual(candidate["name"],
                         "far-band signed-balance lower bound")
        self.assertIn("far band", candidate["mechanism"])
        self.assertIn("tail control is not the finite separator",
                      candidate["prediction"])


if __name__ == "__main__":
    unittest.main()
