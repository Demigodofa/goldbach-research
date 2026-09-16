import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-puncture-denominator-cause-audit.json")


class MobiusMomentSquareDegree5PunctureDenominatorCauseAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.summary = cls.receipt["puncture_summaries"][0]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_puncture_denominator_cause")
        self.assertTrue(self.receipt["finite_denominator_cause_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["source_window_implication_theorem_proved"])
        self.assertFalse(self.receipt["denominator_phase_theorem_proved"])

    def test_puncture_has_four_reduced_denominators(self):
        self.assertEqual(self.receipt["puncture_count"], 1)
        self.assertEqual(self.summary["scale_modulus"], 149)
        self.assertEqual(self.summary["prime_modulus"], 163)
        self.assertEqual(self.summary["label"], "00,12")
        self.assertEqual(
            self.summary["reduced_denominators"],
            [6006, 10010, 15015, 30030])
        self.assertEqual(self.summary["reduced_denominator_count"], 4)

    def test_denominator_sums_reproduce_puncture_totals(self):
        totals = self.summary["totals_by_start"]
        self.assertAlmostEqual(
            totals["0"]["half_frame_contribution"],
            -26177271852.077156,
            places=3)
        self.assertAlmostEqual(
            totals["1"]["half_frame_contribution"],
            595626329.758812,
            places=3)
        self.assertAlmostEqual(
            totals["2"]["half_frame_contribution"],
            -5063730056.479225,
            places=3)
        self.assertAlmostEqual(
            totals["32"]["half_frame_contribution"],
            -259493747123.1459,
            places=3)
        self.assertFalse(totals["1"]["dominates_one_half_signed_full"])
        self.assertTrue(totals["0"]["dominates_one_half_signed_full"])
        self.assertTrue(totals["2"]["dominates_one_half_signed_full"])
        self.assertTrue(totals["32"]["dominates_one_half_signed_full"])

    def test_left_neighbor_failure_is_dominated_by_denominator_30030(self):
        self.assertEqual(
            self.receipt["left_neighbor_dominant_denominator"], 30030)
        transition = self.summary["left_neighbor_transition"][0]
        self.assertEqual(transition["reduced_denominator"], 30030)
        self.assertAlmostEqual(
            transition["failure_minus_comparison_half_frame"],
            19921005797.544876,
            places=3)
        self.assertGreater(
            transition["signed_share_of_total_delta"], 0.70)

    def test_right_neighbor_failure_is_not_same_single_denominator_story(self):
        self.assertEqual(
            self.receipt["right_neighbor_dominant_denominator"], 10010)
        top = self.summary["right_neighbor_transition"][0]
        second = self.summary["right_neighbor_transition"][1]
        third = self.summary["right_neighbor_transition"][2]
        self.assertEqual(top["reduced_denominator"], 10010)
        self.assertEqual(second["reduced_denominator"], 6006)
        self.assertEqual(third["reduced_denominator"], 30030)
        self.assertGreater(
            top["failure_minus_comparison_half_frame"], 0.0)
        self.assertGreater(
            second["failure_minus_comparison_half_frame"], 0.0)
        self.assertLess(
            third["failure_minus_comparison_half_frame"], 0.0)

    def test_candidate_is_finite_mechanism_not_theorem(self):
        candidate = self.receipt["candidate"]
        self.assertEqual(
            candidate["name"], "denominator-phase source admissibility")
        self.assertEqual(candidate["novelty_label"], "new-to-this-task")
        self.assertIn("diffuse across many reduced denominators",
                      candidate["falsifier"])


if __name__ == "__main__":
    unittest.main()
