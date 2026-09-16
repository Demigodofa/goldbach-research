import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.json")


class MobiusMomentSquareDegree5Q46189FarBandSliceBalanceTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_far_band_slice_balance")
        self.assertTrue(
            self.receipt["finite_far_band_slice_balance_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["distance_slice_positive_share_theorem_proved"])
        self.assertFalse(
            self.receipt["distance_slice_pressure_theorem_proved"])
        self.assertFalse(self.receipt["far_band_pressure_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_best_local_witness_is_50a_to_60a(self):
        best = self.receipt["best_single_slice_separating_by_both"]
        self.assertEqual(best["slice_name"], "50A_to_60A")
        self.assertEqual(best["distance_range"], [2151, 2580])
        self.assertAlmostEqual(
            best["adverse_positive_fraction"],
            0.3704750044709434,
            places=15)
        self.assertAlmostEqual(
            best["minimum_replacement_positive_fraction"],
            0.41193052224841337,
            places=15)
        self.assertEqual(
            best["minimum_replacement_positive_fraction_denominator"],
            49742)
        self.assertAlmostEqual(
            best["positive_fraction_gap"],
            0.041455517777469975,
            places=15)
        self.assertAlmostEqual(
            best["adverse_total_over_diagonal"],
            -0.08597078804878477,
            places=15)
        self.assertAlmostEqual(
            best["minimum_replacement_total_over_diagonal"],
            -0.019836945709586308,
            places=15)
        self.assertEqual(best["minimum_replacement_total_denominator"],
                         40755)
        self.assertTrue(best["separates_by_both_share_and_total"])

    def test_only_two_single_slices_separate_by_both(self):
        classification = self.receipt["classification"]
        self.assertEqual(
            classification["single_slices_separating_by_both"],
            ["50A_to_60A", "80A_to_90A"])
        self.assertEqual(
            classification["single_slices_separating_by_both_count"],
            2)
        self.assertTrue(classification["best_slice_is_50A_to_60A"])

    def test_total_only_slice_is_not_promoted(self):
        total_best = self.receipt["best_single_slice_by_total_gap"]
        self.assertEqual(total_best["slice_name"], "10A_to_20A")
        self.assertTrue(total_best["total_pressure_separates"])
        self.assertFalse(total_best["positive_fraction_separates"])
        self.assertFalse(total_best["separates_by_both_share_and_total"])
        self.assertLess(total_best["positive_fraction_gap"], 0.0)

    def test_next_action_targets_50a_to_60a(self):
        candidate = self.receipt["candidate_next_action"]
        self.assertEqual(candidate["name"],
                         "50A-to-60A signed-balance witness")
        self.assertIn("50A..60A", candidate["mechanism"])
        self.assertIn("80A..90A", candidate["prediction"])


if __name__ == "__main__":
    unittest.main()
