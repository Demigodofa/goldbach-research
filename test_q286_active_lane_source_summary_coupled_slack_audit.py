import json
import unittest

from tools.build_q286_active_lane_source_summary_coupled_slack_audit import (
    OUT,
    SOURCE,
    collect_active_source_summary_rows,
    load_json,
)


class Q286ActiveLaneSourceSummaryCoupledSlackAuditTest(unittest.TestCase):

    def test_source_summary_active_row_collection_is_stable(self):
        source = load_json(SOURCE)
        rows, duplicate_count, active_by_block, unique_by_block = (
            collect_active_source_summary_rows(source))
        self.assertEqual(len(rows), 226)
        self.assertEqual(duplicate_count, 0)
        self.assertEqual(
            [row["target"] for row in rows[:5]],
            [90236, 90644, 91082, 91286, 91502])
        self.assertEqual(
            [row["target"] for row in rows[-5:]],
            [805682, 818528, 828418, 846632, 955832])
        self.assertEqual(unique_by_block[1], 36)
        self.assertEqual(unique_by_block[11], 1)
        self.assertEqual(active_by_block[4], 32)

    def test_checked_receipt_records_broadened_coupled_slack_boundary(self):
        self.assertTrue(OUT.exists())
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        self.assertEqual(
            receipt["unique_active_source_summary_row_count"], 226)
        self.assertEqual(receipt["positive_coupled_slack_count"], 83)
        self.assertEqual(receipt["nonpositive_coupled_slack_count"], 143)
        self.assertEqual(receipt["driver_floor_condition_met_count"], 9)
        self.assertEqual(receipt["driver_floor_condition_failed_count"], 217)
        self.assertEqual(receipt["channel_linf_condition_met_count"], 171)
        self.assertEqual(receipt["channel_linf_condition_failed_count"], 55)
        self.assertEqual(
            receipt["negative_driver_rows_with_payment_ratio_count"], 217)
        self.assertEqual(receipt["payment_ratio_above_one_count"], 74)
        self.assertEqual(receipt["payment_ratio_at_or_below_one_count"], 143)
        self.assertEqual(receipt["nonnegative_driver_positive_count"], 9)
        self.assertEqual(
            receipt[
                "payment_ratio_mismatch_count_on_negative_driver_rows"],
            0)
        self.assertEqual(receipt["worst_strict_margin_row"]["target"], 95066)
        self.assertAlmostEqual(
            receipt["worst_strict_margin_row"][
                "strict_closure_margin_to_calibrated_endpoint"],
            -1.3064058812318107)
        self.assertEqual(receipt["best_strict_margin_row"]["target"], 775426)
        self.assertEqual(
            receipt["smallest_positive_strict_margin_row"]["target"],
            395102)
        self.assertEqual(
            receipt["largest_nonpositive_strict_margin_row"]["target"],
            495086)


if __name__ == "__main__":
    unittest.main()
