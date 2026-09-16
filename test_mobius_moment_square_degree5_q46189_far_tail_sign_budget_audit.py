import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-far-tail-sign-budget-audit.json")


class MobiusMomentSquareDegree5Q46189FarTailSignBudgetTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_far_tail_sign_budget")
        self.assertTrue(
            self.receipt["finite_far_tail_sign_budget_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["far_tail_positive_share_theorem_proved"])
        self.assertFalse(
            self.receipt["nonmiddle_positive_share_theorem_proved"])
        self.assertFalse(self.receipt["far_tail_pressure_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_far_tail_positive_share_separates_finite_family(self):
        summary = self.receipt["separation_summary"]
        self.assertAlmostEqual(
            summary["adverse_far_tail_positive_fraction"],
            0.46018216105950077,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_replacement_far_tail_positive_fraction"],
            0.4744728648999872,
            places=15)
        self.assertEqual(
            summary[
                "minimum_replacement_far_tail_positive_fraction_denominator"],
            36465)
        self.assertAlmostEqual(
            summary["far_tail_positive_fraction_gap"],
            0.014290703840486418,
            places=15)
        self.assertTrue(
            summary[
                "adverse_below_far_tail_positive_fraction_separator"])
        self.assertTrue(
            summary[
                "all_replacements_above_far_tail_positive_fraction_separator"])
        self.assertTrue(
            self.receipt["classification"][
                "far_tail_positive_share_separates_finite_family"])

    def test_nonmiddle_positive_share_is_weaker_but_separates(self):
        summary = self.receipt["separation_summary"]
        self.assertAlmostEqual(
            summary["adverse_nonmiddle_positive_fraction"],
            0.4536488257511242,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_replacement_nonmiddle_positive_fraction"],
            0.4562706474233753,
            places=15)
        self.assertEqual(
            summary[
                "minimum_replacement_nonmiddle_positive_fraction_denominator"],
            36465)
        self.assertAlmostEqual(
            summary["nonmiddle_positive_fraction_gap"],
            0.0026218216722511123,
            places=15)
        self.assertTrue(
            self.receipt["classification"][
                "nonmiddle_positive_share_separates_finite_family"])

    def test_negative_envelope_does_not_separate(self):
        non_separators = self.receipt["non_separators"]

        far_tail = non_separators["far_tail_negative_envelope"]
        self.assertFalse(far_tail["separates_adverse_from_replacements"])
        self.assertEqual(far_tail["minimum_replacement_denominator"], 53295)
        self.assertAlmostEqual(
            far_tail["adverse_negative_over_diagonal"],
            -3.9560065034797907,
            places=15)
        self.assertLess(
            far_tail["minimum_replacement_negative_over_diagonal"],
            far_tail["adverse_negative_over_diagonal"])

        nonmiddle = non_separators["nonmiddle_negative_envelope"]
        self.assertFalse(nonmiddle["separates_adverse_from_replacements"])
        self.assertEqual(nonmiddle["minimum_replacement_denominator"], 53295)
        self.assertGreater(
            nonmiddle["minimum_replacement_negative_over_diagonal"],
            nonmiddle["adverse_negative_over_diagonal"])

    def test_next_action_targets_signed_balance(self):
        candidate = self.receipt["candidate_next_action"]
        self.assertEqual(candidate["name"],
                         "broad signed-balance lower bound")
        self.assertIn("positive broad far-tail", candidate["mechanism"])
        self.assertIn("not just the negative envelope",
                      candidate["prediction"])


if __name__ == "__main__":
    unittest.main()
