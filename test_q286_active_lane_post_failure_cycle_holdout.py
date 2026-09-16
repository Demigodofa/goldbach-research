import json
import unittest

from tools.build_q286_active_lane_post_failure_cycle_holdout import (
    OUT,
    POST_FAILURE_START,
    POST_SOURCE_MAX_START,
    TARGETS_PER_CYCLE,
)


class Q286ActiveLanePostFailureCycleHoldoutTest(unittest.TestCase):

    def test_checked_receipt_records_predeclared_full_cycle_outcome(self):
        self.assertTrue(OUT.exists())
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        self.assertEqual(
            receipt["predeclared_windows"]["windows"][
                "first_full_cycle_after_largest_source_failure"],
            POST_FAILURE_START)
        self.assertEqual(
            receipt["predeclared_windows"]["windows"][
                "first_full_cycle_after_source_summary_maximum"],
            POST_SOURCE_MAX_START)
        self.assertEqual(
            receipt["scanned_target_count"], 2 * TARGETS_PER_CYCLE)
        self.assertEqual(receipt["first_three_tail_count"], 1)
        self.assertEqual(receipt["active_selector_count"], 1)
        self.assertEqual(receipt["active_targets"], [650476])
        self.assertEqual(
            receipt["active_targets_already_in_source_summary"], [650476])
        self.assertEqual(receipt["active_targets_not_in_source_summary"], [])
        self.assertEqual(
            receipt["positive_strict_margin_targets"], [650476])
        self.assertEqual(receipt["nonpositive_strict_margin_targets"], [])
        self.assertTrue(
            receipt["all_active_targets_have_positive_strict_margin"])

    def test_active_row_is_direct_validated_and_has_positive_coupled_slack(self):
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        validation = receipt["active_selector_validation"]
        self.assertEqual(validation["validated_target_count"], 1)
        self.assertLessEqual(validation["maximum_first_two_delta"], 1e-12)
        self.assertLessEqual(validation["maximum_first_three_delta"], 1e-12)
        self.assertLessEqual(validation["maximum_full_delta"], 1e-12)
        row = receipt["closure_rows"][0]
        self.assertEqual(row["target"], 650476)
        self.assertAlmostEqual(
            row["first_two_modes_to_principal_ratio"],
            -0.3407986748203168)
        self.assertAlmostEqual(
            row["first_three_modes_to_principal_ratio"],
            -0.3387236396415376)
        self.assertAlmostEqual(
            row["strict_closure_margin_to_calibrated_endpoint"],
            0.39659221326668603)
        self.assertTrue(row["strict_closure_margin_positive"])

    def test_later_full_cycle_is_support_starved(self):
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        later = next(
            window for window in receipt["window_summaries"]
            if window["name"] == "first_full_cycle_after_source_summary_maximum")
        self.assertEqual(later["start"], POST_SOURCE_MAX_START)
        self.assertEqual(later["first_three_tail_count"], 0)
        self.assertEqual(later["active_selector_count"], 0)
        self.assertEqual(later["minimum_first_three_row"]["target"], 957722)
        self.assertAlmostEqual(
            later["minimum_first_three_row"][
                "first_three_modes_to_principal_ratio"],
            -0.26659716030658176)


if __name__ == "__main__":
    unittest.main()
