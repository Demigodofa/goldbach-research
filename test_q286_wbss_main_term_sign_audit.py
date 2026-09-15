import json
import unittest
from pathlib import Path


class Q286WbssMainTermSignAuditTests(unittest.TestCase):
    def test_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-main-term-sign-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["wbss_theorem_proved"])
        self.assertFalse(receipt["binary_distribution_theorem_proved"])
        self.assertIn("finite q286-WBSS main-term sign audit",
                      receipt["status_boundary"])

    def test_full_witness_has_positive_uniform_main_term(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-main-term-sign-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        full = summary["full"]["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(full["positive_uniform_mean_count"], 196)
        self.assertEqual(full["zero_uniform_mean_count"], 0)
        self.assertEqual(full["negative_uniform_mean_count"], 0)
        self.assertGreater(full["uniform_mean_summary"]["minimum"], 0.0)
        self.assertGreater(
            full["sufficient_l1_budget_summary"]["minimum"], 0.02)

    def test_edge_beta_has_positive_post_discovery_main_term(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-main-term-sign-audit.json"
        ).read_text(encoding="utf-8"))
        beta = receipt["summary"]["edge_beta"]["post_discovery_rows"]
        all_beta = receipt["summary"]["edge_beta"]["all_rows"]

        self.assertEqual(beta["positive_uniform_mean_count"], 196)
        self.assertEqual(beta["zero_uniform_mean_count"], 0)
        self.assertEqual(beta["negative_uniform_mean_count"], 0)
        self.assertEqual(all_beta["negative_uniform_mean_count"], 1)
        self.assertGreater(beta["uniform_mean_summary"]["minimum"], 0.0)
        self.assertGreater(
            beta["sufficient_l1_budget_summary"]["minimum"], 0.026)

    def test_tight_l1_budget_rows_are_recorded(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-main-term-sign-audit.json"
        ).read_text(encoding="utf-8"))
        full_tight = receipt[
            "summary"]["full"]["tightest_post_discovery_l1_budgets"][0]
        beta_tight = receipt[
            "summary"]["edge_beta"]["tightest_post_discovery_l1_budgets"][0]

        self.assertEqual(full_tight["target"], 279994)
        self.assertLess(
            full_tight["sufficient_l1_budget_for_positive_expectation"],
            0.021)
        self.assertEqual(beta_tight["target"], 98216)
        self.assertLess(
            beta_tight["sufficient_l1_budget_for_positive_expectation"],
            0.027)


if __name__ == "__main__":
    unittest.main()
