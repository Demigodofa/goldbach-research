import json
import unittest
from pathlib import Path


class Q286AntiLandingSourceBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-anti-landing-source-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["anti_landing_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn(
            "near-sharp", receipt["decision"])

    def test_post_discovery_population_is_expected_size(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(summary["discovery_target_count"], 34)

    def test_tightest_symmetric_budget_is_sub_percent(self):
        receipt = self.load_receipt()
        post = receipt["summary"]["post_discovery_rows"]
        tight = post["tightest_symmetric_budget_row"]

        self.assertEqual(tight["target"], 94856)
        self.assertAlmostEqual(
            tight["positive_to_negative_rescue_ratio"],
            1.0191444227555964)
        self.assertAlmostEqual(
            tight["symmetric_relative_error_budget"],
            0.009481452906409388)
        self.assertEqual(
            post["needs_sub_percent_symmetric_control_count"], 1)
        self.assertEqual(
            post["needs_sub_five_percent_symmetric_control_count"], 2)

    def test_one_sided_budgets_are_recorded(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["post_discovery_rows"][
            "tightest_symmetric_budget_row"]

        self.assertAlmostEqual(
            tight["positive_loss_budget_if_negative_exact"],
            0.018784773474983696)
        self.assertAlmostEqual(
            tight["negative_inflation_budget_if_positive_exact"],
            0.019144422755596365)


if __name__ == "__main__":
    unittest.main()
