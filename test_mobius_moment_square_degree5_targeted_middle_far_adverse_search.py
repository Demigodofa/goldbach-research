import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-targeted-middle-far-adverse-search.json")


class MobiusMomentSquareDegree5TargetedMiddleFarAdverseSearchTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_targeted_middle_far_adverse_search")
        self.assertTrue(self.receipt["finite_targeted_search_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["replacement_family_payment_theorem_proved"])
        self.assertFalse(self.receipt["middle_far_lower_bound_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_selection_and_counts_are_pinned(self):
        self.assertEqual(self.receipt["selected_row_count"], 7)
        self.assertEqual(self.receipt["computed_missing_summary_count"], 1)
        self.assertEqual(
            self.receipt["middle_far_adverse_selected_row_count"], 1)
        self.assertEqual(
            self.receipt["new_middle_far_adverse_selected_row_count"], 0)

    def test_known_q46189_is_recovered_and_no_new_example_found(self):
        classification = self.receipt["classification"]
        adverse_rows = self.receipt["middle_far_adverse_rows"]

        self.assertTrue(classification["known_q46189_recovered"])
        self.assertFalse(
            classification["additional_middle_far_adverse_example_found"])
        self.assertTrue(
            classification["all_new_selected_adverse_mass_near_threshold"])
        self.assertEqual(len(adverse_rows), 1)
        row = adverse_rows[0]
        self.assertEqual(row["scale_modulus"], 229)
        self.assertEqual(row["prime_modulus"], 379)
        self.assertEqual(row["weakest_label"], "00,12")
        self.assertEqual(
            row["clearance_summary"]["largest_middle_negative"][
                "reduced_denominator"],
            46189)

    def test_missing_computed_candidate_is_m353_p691_near_only(self):
        computed = [
            row for row in self.receipt["selected_rows"]
            if row["clearance_summary"]["summary_source"]
            == "computed_in_targeted_search"
        ]
        self.assertEqual(len(computed), 1)
        row = computed[0]
        self.assertEqual(row["scale_modulus"], 353)
        self.assertEqual(row["prime_modulus"], 691)
        counts = row["clearance_summary"][
            "negative_denominator_family_counts"]
        self.assertEqual(
            counts, {"far_3_plus": 0, "middle_2_to_3": 0, "near_1_to_2": 1})
        self.assertAlmostEqual(
            row["clearance_summary"][
                "near_negative_over_middle_far_positive"],
            0.00014712687038539302)

    def test_next_action_is_symbolic_q46189(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"], "symbolic Q46189 replacement-family inequality")
        self.assertIn("before adding more broad finite scans",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
