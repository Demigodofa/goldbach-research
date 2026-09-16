import json
import unittest
from pathlib import Path


class Q286DirectWitnessSignSplitBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-direct-witness-sign-split-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["direct_witness_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("not an easier route", receipt["decision"])

    def test_population_and_positive_counts(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["post_discovery_row_count"], 196)
        self.assertEqual(
            summary["full"]["direct_witness_positive_count"], 196)
        self.assertEqual(
            summary["edge_beta"]["direct_witness_positive_count"], 196)

    def test_full_sign_split_is_tighter_than_anti_landing(self):
        receipt = self.load_receipt()
        anti_budget = receipt["anti_landing_reference"][
            "tightest_symmetric_budget"]
        full_tight = receipt["summary"]["full"]["tightest_symmetric_budget_row"]

        self.assertEqual(full_tight["target"], 94856)
        self.assertAlmostEqual(
            full_tight["positive_to_negative_ratio"],
            1.0145084566730913)
        self.assertAlmostEqual(
            full_tight["symmetric_relative_error_budget"],
            0.007201983503733535)
        self.assertLess(
            full_tight["symmetric_relative_error_budget"], anti_budget)

    def test_edge_beta_reproduces_anti_landing_budget(self):
        receipt = self.load_receipt()
        anti_budget = receipt["anti_landing_reference"][
            "tightest_symmetric_budget"]
        edge_tight = receipt["summary"]["edge_beta"][
            "tightest_symmetric_budget_row"]

        self.assertEqual(edge_tight["target"], 94856)
        self.assertAlmostEqual(
            edge_tight["positive_to_negative_ratio"],
            1.0191444227555964)
        self.assertAlmostEqual(
            edge_tight["symmetric_relative_error_budget"], anti_budget)


if __name__ == "__main__":
    unittest.main()
