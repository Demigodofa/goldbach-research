import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-residue-gap-pressure-separation-audit.json")


class MobiusMomentSquareDegree5Q46189ResidueGapPressureSeparationTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_residue_gap_pressure_separation")
        self.assertTrue(
            self.receipt["finite_residue_gap_pressure_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["far_tail_pressure_theorem_proved"])
        self.assertFalse(self.receipt["nonmiddle_pressure_theorem_proved"])
        self.assertFalse(
            self.receipt["replacement_residue_gap_bound_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_far_tail_pressure_separates_finite_family(self):
        summary = self.receipt["separation_summary"]
        self.assertAlmostEqual(
            summary["adverse_far_tail_over_diagonal"],
            -0.5836029061666043,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_replacement_far_tail_over_diagonal"],
            -0.26234837388449833,
            places=15)
        self.assertEqual(
            summary["minimum_replacement_far_tail_denominator"], 62985)
        self.assertAlmostEqual(
            summary["far_tail_separation_gap"],
            0.32125453228210593,
            places=15)
        self.assertTrue(summary["adverse_below_far_tail_separator"])
        self.assertTrue(summary["all_replacements_above_far_tail_separator"])
        self.assertTrue(
            self.receipt["classification"][
                "far_tail_pressure_separates_finite_family"])

    def test_nonmiddle_pressure_separates_finite_family(self):
        summary = self.receipt["separation_summary"]
        self.assertAlmostEqual(
            summary["adverse_nonmiddle_over_diagonal"],
            -0.721340442056593,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_replacement_nonmiddle_over_diagonal"],
            -0.3390532066023492,
            places=15)
        self.assertEqual(
            summary["minimum_replacement_nonmiddle_denominator"], 36465)
        self.assertAlmostEqual(
            summary["nonmiddle_separation_gap"],
            0.38228723545424376,
            places=15)
        self.assertTrue(summary["adverse_below_nonmiddle_separator"])
        self.assertTrue(
            summary["all_replacements_above_nonmiddle_separator"])
        self.assertTrue(
            self.receipt["classification"][
                "nonmiddle_pressure_separates_finite_family"])

    def test_middle_and_single_top_gap_do_not_separate(self):
        non_separators = self.receipt["non_separators"]
        middle = non_separators["middle_bucket_alone"]
        self.assertFalse(middle["separates_adverse_from_replacements"])
        self.assertEqual(middle["minimum_replacement_middle_denominator"],
                         38038)
        self.assertLess(
            middle["minimum_replacement_middle_over_diagonal"],
            middle["adverse_middle_over_diagonal"])

        top_gap = non_separators["single_top_negative_gap"]
        self.assertFalse(top_gap["separates_adverse_from_replacements"])
        self.assertEqual(
            top_gap["minimum_replacement_top_negative_denominator"], 38038)
        self.assertLess(
            top_gap["minimum_replacement_top_negative_pair_over_diagonal"],
            top_gap["adverse_top_negative_pair_over_diagonal"])

    def test_candidate_next_target_is_broad_pressure(self):
        mechanism = self.receipt["mechanism_under_test"]
        self.assertEqual(mechanism["name"],
                         "broad far-tail residue-gap overpayment")
        self.assertIn("far+tail", mechanism["falsifier"])
        self.assertIn("single largest negative residue gap",
                      mechanism["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
