import json
import unittest
from pathlib import Path


class Q286OrthogonalResidualSignSplitBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-orthogonal-residual-sign-split-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_residual_sign_split_is_sharper_but_still_near_sharp")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(
            receipt["orthogonal_residual_lower_tail_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("still near-sharp", receipt["decision"])

    def test_population_and_reconstruction(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["target_count"], 7)
        self.assertEqual(summary["actual_full_positive_count"], 5)
        self.assertEqual(summary["actual_full_nonpositive_count"], 2)
        self.assertLess(summary["maximum_reconstruction_error"], 1e-12)
        for row in receipt["target_rows"]:
            self.assertAlmostEqual(
                row["aligned_only_full_action_to_principal"]
                + row["positive_residual_contribution"]
                - row["negative_residual_drag"],
                row["actual_full_action"])

    def test_tightest_budget_is_94856_and_sub_percent(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["tightest_positive_symmetric_budget_row"]

        self.assertEqual(tight["target"], 94856)
        self.assertAlmostEqual(
            tight["symmetric_positive_negative_error_budget_with_aligned_exact"],
            0.009396193466872777)
        self.assertLess(
            tight["symmetric_positive_negative_error_budget_with_aligned_exact"],
            0.01)
        self.assertTrue(tight["needs_sub_percent_symmetric_control"])

    def test_residual_split_is_looser_than_raw_full_but_not_escape(self):
        receipt = self.load_receipt()
        raw = receipt["raw_full_sign_split_reference"][
            "tightest_symmetric_budget"]
        residual = receipt["summary"]["tightest_positive_symmetric_budget_row"][
            "symmetric_positive_negative_error_budget_with_aligned_exact"]

        self.assertAlmostEqual(raw, 0.007201983503733535)
        self.assertGreater(residual, raw)
        self.assertLess(residual, 0.01)
        self.assertEqual(
            receipt["summary"]["needs_sub_percent_symmetric_control_count"],
            1)
        self.assertEqual(
            receipt["summary"]["needs_sub_five_percent_symmetric_control_count"],
            1)


if __name__ == "__main__":
    unittest.main()
