import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-margin-m383-clearance-holdout.json")


class MobiusMomentSquareDegree5SourceMarginM383ClearanceHoldoutTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "HOLDOUT_degree5_source_margin_m383_clearance_family")
        self.assertTrue(self.receipt["fresh_clearance_holdout_only"])
        self.assertTrue(self.receipt["finite_holdout_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["clearance_family_theorem_proved"])

    def test_holdout_targets_m383_tight_block(self):
        self.assertEqual(self.receipt["scale_modulus"], 383)
        self.assertEqual(self.receipt["prime_modulus"], 599)
        self.assertEqual(self.receipt["weakest_label"], "00,12")

    def test_clearance_family_target_survives(self):
        self.assertTrue(
            self.receipt["all_negative_denominators_near_threshold"])
        self.assertTrue(
            self.receipt["middle_far_positive_dominates_near_negative"])
        self.assertTrue(
            self.receipt["middle_far_total_dominates_near_negative"])
        self.assertAlmostEqual(
            self.receipt["near_negative_abs"], 152079879558.52072)
        self.assertAlmostEqual(
            self.receipt["middle_far_total_margin_sum"],
            203565211531254.94)
        self.assertAlmostEqual(
            self.receipt["near_negative_over_middle_far_positive"],
            0.0007470818732461599)

    def test_family_counts_are_pinned(self):
        families = self.receipt["scale_summary"]["family_summaries"]
        self.assertEqual(families["near_1_to_2"]["row_count"], 38)
        self.assertEqual(families["near_1_to_2"]["negative_count"], 3)
        self.assertEqual(families["middle_2_to_3"]["row_count"], 19)
        self.assertEqual(families["middle_2_to_3"]["negative_count"], 0)
        self.assertEqual(families["far_3_plus"]["row_count"], 13)
        self.assertEqual(families["far_3_plus"]["negative_count"], 0)
        self.assertEqual(
            families["near_1_to_2"]["largest_negative"][
                "reduced_denominator"],
            52003)


if __name__ == "__main__":
    unittest.main()
