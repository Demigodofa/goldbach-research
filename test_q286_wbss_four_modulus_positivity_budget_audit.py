import json
import unittest
from pathlib import Path


class Q286WbssFourModulusPositivityBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-positivity-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["independence_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite q286-WBSS four-modulus",
                      receipt["status_boundary"])

    def test_combines_initial_and_far_lift_holdouts(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]
        by_source = receipt["holdout"]["summary_by_source"]

        self.assertEqual(receipt["holdout"]["source_count"], 2)
        self.assertEqual(summary["row_count"], 232)
        self.assertEqual(set(by_source), {
            "initial_residue_lift_holdout",
            "far_lift_holdout",
        })
        self.assertEqual(
            by_source["initial_residue_lift_holdout"]["row_count"], 116)
        self.assertEqual(by_source["far_lift_holdout"]["row_count"], 116)

    def test_z_below_three_is_falsified_but_budget_survives(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["z_below_three_cap_falsified"])
        self.assertTrue(
            receipt["positivity_budget_survives_combined_holdouts"])
        self.assertEqual(summary["actual_positive_count"], 232)
        self.assertEqual(summary["actual_nonpositive_count"], 0)
        self.assertGreater(summary["z_below_three_failure_count"], 0)
        self.assertEqual(summary["budget_failure_count"], 0)
        self.assertEqual(summary["signed_ratio_failure_count"], 0)

    def test_budget_ratio_is_lambda_phi(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertLess(
            summary["lambda_budget_abs_error_summary"]["maximum"],
            1e-12)
        self.assertEqual(
            summary["largest_signed_budget_ratio_row"]["target"], 1002478)
        self.assertAlmostEqual(
            summary["signed_budget_ratio_summary"]["maximum"],
            0.29444884696113977,
            places=12)

    def test_tightest_sigma_margin_is_recorded(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["tightest_sigma_margin_row"]["target"],
                         1001554)
        self.assertGreater(
            summary["positivity_margin_sigma_summary"]["minimum"], 7.0)


if __name__ == "__main__":
    unittest.main()
