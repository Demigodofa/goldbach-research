import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueRawBudgetScheduleTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-raw-budget-schedule.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_budget_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_zero_residue_raw_discrepancy_budget_schedule_unproved")
        self.assertFalse(
            receipt["zero_residue_raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["binary_prime_moment_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_zero_lane_budget_numbers_are_pinned(self):
        receipt = self.load_receipt()
        budget = receipt["coefficient_l1_budget"]
        schedule = receipt["zero_residue_schedule"]

        self.assertEqual(schedule["target_mod_286"], 0)
        self.assertEqual(schedule["period"], 10010)
        self.assertEqual(schedule["period_residue_count"], 35)
        self.assertAlmostEqual(
            budget["total_l1_norm"], 372.962002076135, places=12)
        self.assertAlmostEqual(
            budget["global_all_residue_uniform_cap"],
            0.0016192946592982506,
            places=15)
        self.assertAlmostEqual(
            schedule["local_main_summary"]["minimum"],
            0.7140019401930207,
            places=12)
        self.assertAlmostEqual(
            schedule["uniform_cap_summary"]["minimum"],
            0.0019144093398749697,
            places=15)

    def test_tightest_and_loosest_period_residues_are_pinned(self):
        receipt = self.load_receipt()
        schedule = receipt["zero_residue_schedule"]
        tight = schedule["tightest_budget_row"]
        loose = schedule["loosest_budget_row"]

        self.assertEqual(tight["target_residue"], 9724)
        self.assertEqual(tight["period_residue_index"], 34)
        self.assertAlmostEqual(
            tight["cap_relaxation_factor_vs_global_cap"],
            1.1822489062642942,
            places=12)
        self.assertEqual(loose["target_residue"], 1716)
        self.assertEqual(loose["period_residue_index"], 6)
        self.assertAlmostEqual(
            loose["uniform_residue_error_cap"],
            0.0034092658993930512,
            places=15)

    def test_zero_lane_is_not_worse_than_global_l1_budget(self):
        receipt = self.load_receipt()
        comparison = receipt["comparison_to_global_budget"]

        self.assertFalse(
            comparison["zero_lane_is_worse_than_global_l1_budget"])
        self.assertGreater(
            comparison["zero_lane_tightest_cap"],
            comparison["global_all_residue_cap"])
        self.assertAlmostEqual(
            comparison["zero_lane_tightest_cap_relaxation_factor"],
            1.1822489062642942,
            places=12)
        self.assertIn("not captured by this crude total-L1 budget",
                      comparison["interpretation"])
        self.assertIn("signed/character", receipt["decision"])


if __name__ == "__main__":
    unittest.main()
