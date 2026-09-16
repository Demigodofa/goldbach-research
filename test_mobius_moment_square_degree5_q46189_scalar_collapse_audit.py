import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-scalar-collapse-audit.json")


class MobiusMomentSquareDegree5Q46189ScalarCollapseAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_cellwise_scalar_collapse")
        self.assertTrue(self.receipt["finite_scalar_collapse_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["exact_scalar_identity_theorem_proved"])
        self.assertFalse(
            self.receipt["symbolic_replacement_ratio_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_cellwise_scalar_collapse(self):
        q_row = self.receipt["q46189_scalar_row"]
        classification = self.receipt["classification"]

        self.assertEqual(q_row["reduced_denominator"], 46189)
        self.assertEqual(q_row["zero_left_cell_count"], 0)
        self.assertAlmostEqual(
            q_row["cellwise_scalar_real"],
            -0.07475328212536139)
        self.assertLess(abs(q_row["cellwise_scalar_imag"]), 1e-18)
        self.assertLess(
            q_row["max_abs_cellwise_scalar_deviation"],
            1.1e-13)
        self.assertTrue(q_row["cellwise_scalar_negative_real"])
        self.assertTrue(
            q_row["cellwise_scalar_collapse_verified_to_tolerance"])
        self.assertTrue(classification["q46189_cellwise_scalar_collapse"])

    def test_cross_ratio_reduces_to_one_coordinate_ratio(self):
        rows = [
            self.receipt["q46189_scalar_row"],
            *self.receipt["replacement_scalar_rows"],
        ]
        classification = self.receipt["classification"]

        self.assertTrue(
            classification["all_rows_ratio_reduces_to_one_coordinate"])
        for row in rows:
            self.assertLess(row["ratio_reduction_abs_error"], 1e-15)
            self.assertAlmostEqual(
                row["one_coordinate_active_over_full_ratio"],
                row["cross_active_over_full_ratio"])
            self.assertTrue(row["full_contribution_negative"])
            self.assertTrue(row["ratio_side_explains_margin_sign"])

    def test_replacements_collapse_and_stay_above_half(self):
        rows = self.receipt["replacement_scalar_rows"]
        classification = self.receipt["classification"]

        self.assertEqual(len(rows), 10)
        self.assertTrue(
            classification["all_replacements_cellwise_scalar_collapse"])
        self.assertTrue(classification["all_replacements_ratio_above_half"])
        self.assertAlmostEqual(
            min(row["ratio_minus_half"] for row in rows),
            0.07635340770691146)
        self.assertAlmostEqual(
            max(row["ratio_minus_half"] for row in rows),
            0.5735414442150175)
        self.assertLess(
            max(row["max_abs_cellwise_scalar_deviation"] for row in rows),
            3.8e-13)

    def test_each_omitted_high_prime_family_collapses(self):
        families = self.receipt[
            "omitted_high_prime_family_scalar_summaries"]

        self.assertEqual(set(families), {"11", "13", "17", "19"})
        self.assertAlmostEqual(
            families["17"]["minimum_ratio_minus_half"],
            0.07635340770691146)
        for summary in families.values():
            self.assertTrue(summary["all_rows_cellwise_scalar_collapse"])
            self.assertLess(
                summary["maximum_ratio_reduction_abs_error"], 1e-15)

    def test_next_action_is_exact_divisor_pair_identity(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(action["name"], "exact divisor-pair scalar identity")
        self.assertIn("source-pair level", action["mechanism"])
        self.assertIn("before reduced-residue aggregation",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
