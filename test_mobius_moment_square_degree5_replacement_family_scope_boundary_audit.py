import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-replacement-family-scope-boundary-audit.json")


class MobiusMomentSquareDegree5ReplacementFamilyScopeBoundaryAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_replacement_family_scope_boundary")
        self.assertTrue(self.receipt["finite_scope_boundary_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["replacement_family_payment_theorem_proved"])
        self.assertFalse(self.receipt["near_adverse_upper_bound_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_source_scope_has_single_middle_far_exception(self):
        source = self.receipt["source_scope"]
        row = source["middle_far_negative_rows"][0]

        self.assertEqual(source["checked_row_count"], 6)
        self.assertEqual(
            source["negative_denominator_family_counts"],
            {"far_3_plus": 0, "middle_2_to_3": 1, "near_1_to_2": 17})
        self.assertEqual(source["middle_far_negative_row_count"], 1)
        self.assertEqual(row["scale_modulus"], 229)
        self.assertEqual(row["prime_modulus"], 379)
        self.assertEqual(row["weakest_label"], "00,12")
        self.assertEqual(
            row["largest_middle_negative"]["reduced_denominator"], 46189)

    def test_band_scope_has_same_middle_far_exception(self):
        band = self.receipt["band_scope"]
        row = band["middle_far_negative_rows"][0]
        classification = self.receipt["classification"]

        self.assertEqual(band["checked_row_count"], 4)
        self.assertEqual(
            band["negative_denominator_family_counts"],
            {"far_3_plus": 0, "middle_2_to_3": 1, "near_1_to_2": 17})
        self.assertEqual(band["middle_far_negative_row_count"], 1)
        self.assertEqual(row["band"], "sigma_1_50_1_75")
        self.assertEqual(row["scale_modulus"], 229)
        self.assertEqual(row["prime_modulus"], 379)
        self.assertEqual(
            row["largest_middle_negative"]["reduced_denominator"], 46189)
        self.assertTrue(
            classification["same_q46189_exception_in_source_and_band"])
        self.assertTrue(
            classification[
                "q46189_payment_is_single_current_middle_far_exemplar"])

    def test_q46189_payment_summary_is_carried_forward(self):
        summary = self.receipt["q46189_payment_summary"]

        self.assertAlmostEqual(
            summary["replacement_payment_over_defect"],
            1740.1304948156007)
        self.assertAlmostEqual(
            summary["minimum_individual_payment_over_defect"],
            36.74165224066973)
        self.assertTrue(
            summary["each_omitted_high_prime_family_pays_defect"])

    def test_next_action_preserves_theorem_boundary(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"], "replacement-family theorem boundary split")
        self.assertIn("additional middle/far adverse exemplars",
                      action["prediction"])
        self.assertIn("symbolic Q=46189 replacement-family inequality",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
