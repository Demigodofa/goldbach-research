import json
import unittest
from pathlib import Path


class Q286Wbss1113EdgeResidualBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-1113-edge-residual-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["lead_edge_theorem_proved"])
        self.assertFalse(receipt["residual_budget_theorem_proved"])
        self.assertFalse(receipt["character_sum_bound_proved"])
        self.assertFalse(
            receipt["binary_prime_projection_control_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite q286-WBSS 11,13 edge residual-budget",
                      receipt["status_boundary"])
        self.assertIn("not universal bounds", receipt["status_boundary"])

    def test_1113_lead_edge_is_negative_on_all_rows(self):
        receipt = self.load_receipt()
        all_rows = receipt["summaries"]["all_dual_edge_rows"]
        post_rows = receipt["summaries"]["post_discovery_rows"]

        self.assertEqual(all_rows["row_count"], 230)
        self.assertEqual(all_rows["lead_edge_negative_count"], 230)
        self.assertEqual(post_rows["row_count"], 196)
        self.assertEqual(post_rows["lead_edge_negative_count"], 196)

    def test_positive_residual_pushback_never_consumes_lead_drag(self):
        receipt = self.load_receipt()
        all_rows = receipt["summaries"]["all_dual_edge_rows"]
        post_rows = receipt["summaries"]["post_discovery_rows"]

        self.assertTrue(receipt["finite_1113_residual_budget_passes"])
        self.assertEqual(
            all_rows["total_edge_negative_after_residual_count"], 230)
        self.assertEqual(
            post_rows["total_edge_negative_after_residual_count"], 196)
        self.assertAlmostEqual(
            all_rows[
                "observed_minimum_passing_theta_for_positive_pushback"],
            0.3895519069948021,
            places=12,
        )
        self.assertGreater(
            all_rows["lead_drag_margin_after_positive_pushback_summary"][
                "minimum"],
            0.2,
        )

    def test_half_theta_passes_but_quarter_theta_fails_finite_fixture(self):
        receipt = self.load_receipt()
        profiles = {
            row["name"]: row
            for row in receipt["summaries"]["all_dual_edge_rows"][
                "threshold_profiles"]
        }

        self.assertFalse(profiles["one_quarter"]["passes_all_rows"])
        self.assertEqual(profiles["one_quarter"]["failing_row_count"], 3)
        self.assertTrue(profiles["one_half"]["passes_all_rows"])
        self.assertEqual(profiles["one_half"]["failing_row_count"], 0)
        self.assertGreater(
            profiles["one_half"]["absolute_slack_against_observed_maximum"],
            0.1,
        )

    def test_absolute_residual_load_is_not_the_right_budget(self):
        receipt = self.load_receipt()
        all_rows = receipt["summaries"]["all_dual_edge_rows"]

        self.assertGreater(
            all_rows["abs_residual_load_to_lead_drag_ratio_summary"][
                "maximum"],
            2.0,
        )
        self.assertLess(
            all_rows["positive_pushback_to_lead_drag_ratio_summary"][
                "maximum"],
            0.5,
        )
        self.assertEqual(all_rows["residual_positive_pushback_row_count"], 32)
        self.assertEqual(all_rows["residual_negative_help_row_count"], 198)


if __name__ == "__main__":
    unittest.main()
