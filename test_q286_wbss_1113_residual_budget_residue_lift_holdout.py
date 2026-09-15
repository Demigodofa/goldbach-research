import json
import unittest
from pathlib import Path


class Q286Wbss1113ResidualBudgetResidueLiftHoldoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-1113-residual-budget-residue-lift-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertTrue(receipt["fresh_holdout_claimed"])
        self.assertFalse(receipt["lead_edge_theorem_proved"])
        self.assertFalse(receipt["residual_budget_theorem_proved"])
        self.assertFalse(receipt["character_sum_bound_proved"])
        self.assertFalse(
            receipt["binary_prime_projection_control_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite targeted q286-WBSS 11,13",
                      receipt["status_boundary"])

    def test_source_selection_targets_positive_pushback_residues(self):
        receipt = self.load_receipt()
        source = receipt["source_population"]

        self.assertEqual(source["row_count"], 230)
        self.assertEqual(source["positive_pushback_row_count"], 32)
        self.assertEqual(source["unique_positive_residue_count"], 32)
        self.assertEqual(receipt["holdout"]["lift_count_per_residue"], 4)
        self.assertEqual(receipt["holdout"]["target_count"], 128)

    def test_holdout_demotes_1113_lead_edge_route(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertFalse(receipt["finite_1113_residual_budget_survives_holdout"])
        self.assertTrue(receipt["lead_edge_route_demoted_by_holdout"])
        self.assertEqual(summary["row_count"], 128)
        self.assertEqual(summary["lead_edge_negative_count"], 56)
        self.assertEqual(summary["lead_edge_nonnegative_count"], 72)
        self.assertEqual(
            summary["total_edge_negative_after_residual_count"], 56)

    def test_theta_half_no_longer_survives_holdout(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]
        profiles = {
            row["name"]: row for row in summary["theta_threshold_profiles"]
        }

        self.assertFalse(receipt["point_5_theta_survives_holdout"])
        self.assertFalse(receipt["point_25_theta_survives_holdout"])
        self.assertFalse(profiles["one"]["passes_all_rows"])
        self.assertEqual(profiles["one_half"]["failing_row_count"], 91)
        self.assertEqual(profiles["one"]["failing_row_count"], 84)
        self.assertAlmostEqual(
            summary[
                "observed_minimum_passing_theta_for_positive_pushback"],
            16.998115502313933,
            places=12,
        )

    def test_lift_buckets_record_failures_across_all_lifts(self):
        receipt = self.load_receipt()
        by_lift = receipt["holdout"]["summary_by_lift"]

        self.assertEqual(
            [by_lift[f"lift_{index}"]["row_count"] for index in range(4)],
            [32, 32, 32, 32],
        )
        self.assertEqual(
            [by_lift[f"lift_{index}"]["lead_edge_negative_count"]
             for index in range(4)],
            [12, 10, 16, 18],
        )
        self.assertEqual(
            [by_lift[f"lift_{index}"][
                "total_edge_negative_after_residual_count"]
             for index in range(4)],
            [9, 11, 19, 17],
        )


if __name__ == "__main__":
    unittest.main()
