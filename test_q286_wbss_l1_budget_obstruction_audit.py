import json
import unittest
from pathlib import Path


class Q286WbssL1BudgetObstructionAuditTests(unittest.TestCase):
    def test_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-l1-budget-obstruction-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["l1_uniformity_bridge_theorem_proved"])
        self.assertTrue(
            receipt["blunt_l1_uniformity_bridge_falsified_as_explanation"])
        self.assertIn("finite q286-WBSS L1-budget obstruction audit",
                      receipt["status_boundary"])

    def test_actual_l1_is_far_outside_post_discovery_budgets(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-l1-budget-obstruction-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        full = summary["full"]["post_discovery_rows"]
        beta = summary["edge_beta"]["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(
            full["actual_l1_within_sufficient_budget_count"], 0)
        self.assertEqual(
            beta["actual_l1_within_sufficient_budget_count"], 0)
        self.assertGreater(
            summary["post_discovery_actual_l1_distance_summary"]["minimum"],
            0.55)
        self.assertLess(
            full["sufficient_l1_budget_summary"]["maximum"], 0.065)
        self.assertLess(
            beta["sufficient_l1_budget_summary"]["maximum"], 0.188)

    def test_signed_expectations_stay_positive_despite_l1_failure(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-l1-budget-obstruction-audit.json"
        ).read_text(encoding="utf-8"))
        full = receipt["summary"]["full"]["post_discovery_rows"]
        beta = receipt["summary"]["edge_beta"]["post_discovery_rows"]

        self.assertEqual(full["actual_positive_count"], 196)
        self.assertEqual(beta["actual_positive_count"], 196)
        self.assertGreater(
            full["actual_expectation_summary"]["minimum"], 0.0)
        self.assertGreater(
            beta["actual_expectation_summary"]["minimum"], 0.0)

    def test_extreme_ratio_rows_are_recorded(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-l1-budget-obstruction-audit.json"
        ).read_text(encoding="utf-8"))
        full_extreme = receipt[
            "summary"]["full"]["largest_post_discovery_l1_to_budget_ratios"][0]
        beta_extreme = receipt[
            "summary"]["edge_beta"][
                "largest_post_discovery_l1_to_budget_ratios"][0]

        self.assertGreater(full_extreme["actual_l1_to_budget_ratio"], 20.0)
        self.assertGreater(beta_extreme["actual_l1_to_budget_ratio"], 15.0)


if __name__ == "__main__":
    unittest.main()
