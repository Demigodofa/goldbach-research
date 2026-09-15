import json
import unittest
from pathlib import Path

from tools.build_q286_active_lane_strict_closure_phase_space_html import (
    OUT as HTML_OUT,
    build_view_model,
    script_json,
)
from tools.build_q286_active_lane_strict_closure_coupled_slack_diagnosis import (
    OUT as COUPLED_SLACK_OUT,
)
from tools.build_q286_active_lane_strict_closure_post_discovery_stress import (
    EVIDENCE,
    OUT,
    SOURCE,
    select_post_discovery_stress_targets,
)


class Q286ActiveLaneStrictClosurePostDiscoveryStressTest(unittest.TestCase):

    def test_selector_recovers_one_worst_active_row_per_post_discovery_block(self):
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        selected = select_post_discovery_stress_targets(source)
        self.assertEqual(
            [row["selected_target"] for row in selected],
            [94856, 194384, 255704, 383486, 480614, 548666,
             594112, 658598, 805682, 846632, 955832])
        self.assertEqual(
            [row["block_index_after_discovery"] for row in selected],
            list(range(1, 12)))
        self.assertTrue(all(
            row["selected_source_row"]["first_two_modes_to_principal_ratio"]
            < -0.2
            and row["selected_source_row"][
                "first_three_modes_to_principal_ratio"] < -0.3
            for row in selected))

    def test_checked_receipt_records_endpoint_falsifiers_and_visual_schema(self):
        self.assertTrue(OUT.exists())
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        self.assertEqual(receipt["scanned_target_count"], 11)
        self.assertEqual(receipt["tail_target_count"], 11)
        self.assertEqual(
            receipt["nonpositive_strict_margin_targets"],
            [94856, 194384, 255704, 383486, 480614, 548666])
        self.assertEqual(
            receipt["positive_strict_margin_targets"],
            [594112, 658598, 805682, 846632, 955832])
        self.assertFalse(receipt[
            "all_tail_targets_have_positive_strict_margin"])
        self.assertAlmostEqual(
            receipt["target_rows"]["94856"][
                "strict_closure_margin_to_calibrated_endpoint"],
            -1.1917268781786845)
        self.assertAlmostEqual(
            receipt["target_rows"]["955832"][
                "strict_closure_margin_to_calibrated_endpoint"],
            0.1327432030991093)
        self.assertEqual(
            receipt["phase_space_visual_schema"]["x"], "log(target)")
        self.assertEqual(len(receipt["phase_space_points"]), 11)
        self.assertTrue(
            (EVIDENCE / "q286-principal-rescue-obstruction-audit.json").exists())

    def test_phase_space_html_view_model_preserves_rows_without_html_escape(self):
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        view = build_view_model(receipt)
        self.assertEqual(len(view["rows"]), 11)
        self.assertEqual(view["rows"][0]["target"], 94856)
        self.assertEqual(view["rows"][0]["detail"]["fixed_conductor_pair"],
                         [35, 77])
        hinge = next(row for row in view["rows"] if row["target"] == 594112)
        self.assertAlmostEqual(hinge["paymentRatio"], 1.036015710699683)
        self.assertAlmostEqual(
            hinge["detail"][
                "derived_channel_payment_ratio_to_driver_deficit"],
            1.036015710699683)
        encoded = script_json(view)
        self.assertIn('"target": 94856', encoded)
        self.assertIn('"paymentRatio": 1.036015710699683', encoded)
        self.assertNotIn("&quot;", encoded)
        self.assertTrue(HTML_OUT.exists())

    def test_coupled_slack_diagnosis_records_visual_hinge(self):
        self.assertTrue(COUPLED_SLACK_OUT.exists())
        receipt = json.loads(COUPLED_SLACK_OUT.read_text(encoding="utf-8"))
        self.assertEqual(receipt["row_count"], 11)
        self.assertEqual(receipt["driver_floor_condition_met_count"], 0)
        self.assertEqual(receipt["channel_linf_condition_met_count"], 8)
        self.assertEqual(receipt["coupled_slack_positive_count"], 5)
        self.assertEqual(receipt["channel_pass_but_coupled_fail_count"], 3)
        self.assertEqual(receipt["first_channel_bound_pass_target"], 383486)
        self.assertEqual(receipt["first_coupled_slack_pass_target"], 594112)
        self.assertTrue(receipt["driver_floor_fails_on_every_stress_row"])
        self.assertEqual(receipt["tightest_passing_row"]["target"], 594112)
        self.assertEqual(receipt["strongest_failing_row"]["target"], 548666)
        hinge = next(row for row in receipt["rows"]
                     if row["target"] == 594112)
        self.assertAlmostEqual(
            hinge["channel_payment_ratio_to_driver_deficit"],
            1.036015710699683)


if __name__ == "__main__":
    unittest.main()
