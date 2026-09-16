import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueCharacterBudgetScheduleTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-character-budget-schedule.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_character_budget_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_zero_residue_character_moment_budget_schedule_unproved")
        self.assertFalse(
            receipt["zero_residue_raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["aggregate_character_moment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["binary_prime_moment_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_global_character_budget_numbers_are_pinned(self):
        receipt = self.load_receipt()
        budget = receipt["coefficient_character_budget"]

        self.assertEqual(budget["active_character_count"], 122)
        self.assertEqual(budget["active_real_channel_count"], 64)
        self.assertAlmostEqual(
            budget["total_character_l1"],
            49.153988812629684,
            places=12)
        self.assertAlmostEqual(
            budget["aggregate_character_l2"],
            5.525106448699807,
            places=12)
        self.assertAlmostEqual(
            budget["global_character_linf_cap"],
            0.012286599575574883,
            places=15)
        self.assertAlmostEqual(
            budget["global_aggregate_character_l2_cap"],
            0.10930746469603118,
            places=15)

    def test_zero_lane_character_schedule_numbers_are_pinned(self):
        receipt = self.load_receipt()
        schedule = receipt["zero_residue_character_schedule"]

        self.assertEqual(schedule["target_mod_286"], 0)
        self.assertEqual(schedule["period"], 10010)
        self.assertEqual(schedule["period_residue_count"], 35)
        self.assertAlmostEqual(
            schedule["character_linf_cap_summary"]["minimum"],
            0.014525818909930746,
            places=15)
        self.assertAlmostEqual(
            schedule["aggregate_character_l2_cap_summary"]["minimum"],
            0.12922863058340583,
            places=14)
        self.assertAlmostEqual(
            schedule["aggregate_l2_vs_residue_l1_cap_summary"]["minimum"],
            67.50313420004822,
            places=10)

    def test_zero_lane_is_not_worse_than_global_character_budget(self):
        receipt = self.load_receipt()
        comparison = receipt["comparison_to_global_character_budget"]
        tight = receipt["zero_residue_character_schedule"][
            "tightest_aggregate_l2_row"]

        self.assertEqual(tight["target_residue"], 9724)
        self.assertEqual(tight["period_residue_index"], 34)
        self.assertFalse(
            comparison["zero_lane_is_worse_than_global_character_budget"])
        self.assertGreater(
            comparison["zero_lane_tightest_aggregate_l2_cap"],
            comparison["global_aggregate_l2_cap"])
        self.assertAlmostEqual(
            comparison["zero_lane_tightest_l2_relaxation_factor"],
            1.1822489062642942,
            places=12)
        self.assertIn("not coefficient-norm size alone",
                      comparison["interpretation"])
        self.assertIn("pointwise raw signed/character",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
