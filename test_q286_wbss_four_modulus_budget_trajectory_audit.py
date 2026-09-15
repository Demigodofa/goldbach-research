import json
import unittest
from pathlib import Path


class Q286WbssFourModulusBudgetTrajectoryAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-budget-trajectory-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["recurrence_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite q286-WBSS four-modulus",
                      receipt["status_boundary"])

    def test_groups_into_29_eight_lift_trajectories(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(receipt["holdout"]["row_count"], 232)
        self.assertEqual(receipt["holdout"]["trajectory_count"], 29)
        self.assertTrue(summary["all_trajectories_have_eight_lifts"])
        self.assertEqual(summary["row_count_summary"]["minimum"], 8)
        self.assertEqual(summary["row_count_summary"]["maximum"], 8)

    def test_no_monotone_trajectory_and_worst_positions_distribute(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["no_monotone_non_decreasing_trajectory"])
        self.assertEqual(
            summary["monotone_non_decreasing_trajectory_count"], 0)
        self.assertTrue(receipt["worst_lift_position_distributed"])
        self.assertEqual(summary["worst_lift_index_counts"], {
            "0": 5,
            "1": 3,
            "2": 5,
            "3": 4,
            "4": 6,
            "5": 2,
            "6": 1,
            "7": 3,
        })

    def test_worst_trajectory_is_recorded(self):
        receipt = self.load_receipt()
        worst = receipt["holdout"]["summary"]["worst_trajectory"]

        self.assertEqual(worst["target_residue"], 1478)
        self.assertEqual(worst["source_positive_target"], 251728)
        self.assertEqual(worst["worst_target"], 1002478)
        self.assertEqual(worst["worst_lift_index"], 4)
        self.assertAlmostEqual(
            worst["max_signed_budget_ratio"],
            0.29444884696113977,
            places=12)

    def test_every_trajectory_remains_positive(self):
        receipt = self.load_receipt()

        self.assertTrue(receipt["all_trajectories_positive"])
        for row in receipt["holdout"]["trajectories"]:
            self.assertGreater(
                row["positivity_margin_sigma_summary"]["minimum"], 0.0)


if __name__ == "__main__":
    unittest.main()
