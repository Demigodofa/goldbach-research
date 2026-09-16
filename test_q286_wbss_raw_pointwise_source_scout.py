import json
import unittest
from pathlib import Path


class Q286WbssRawPointwiseSourceScoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-raw-pointwise-source-scout.json"
        ).read_text(encoding="utf-8"))

    def test_source_scout_is_hold_not_bridge(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SOURCE_SCOUT_no_raw_pointwise_q286_bridge_found")
        self.assertFalse(receipt["external_pointwise_bridge_found"])
        self.assertFalse(
            receipt["signed_weight_major_arc_estimate_proved"])
        self.assertFalse(receipt["raw_weighted_witness_theorem_proved"])
        self.assertFalse(receipt["active_character_moment_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("Source-scout HOLD only",
                      receipt["status_boundary"])

    def test_source_fit_table_is_pinned(self):
        receipt = self.load_receipt()
        rows = {row["id"]: row for row in receipt["source_fit_table"]}

        self.assertEqual(receipt["fit_summary"]["checked_source_count"], 4)
        self.assertEqual(
            receipt["fit_summary"][
                "direct_raw_pointwise_bridge_count"], 0)
        self.assertFalse(
            receipt["fit_summary"][
                "reactivates_q286_signed_weight_lane"])

        self.assertEqual(
            rows["Salmensuu_2021_summands_in_AP"][
                "fit_to_q286_raw_pointwise_trigger"],
            "insufficient")
        self.assertIn(
            "Almost-all",
            rows["Salmensuu_2021_summands_in_AP"]["mismatch"])

        self.assertEqual(
            rows["Halupczok_2012_AP_and_short_intervals"][
                "fit_to_q286_raw_pointwise_trigger"],
            "insufficient")
        self.assertIn(
            "Mean-value",
            rows["Halupczok_2012_AP_and_short_intervals"]["mismatch"])

        self.assertEqual(
            rows["Lichtman_2023_Goldbach_upper_bounds"][
                "fit_to_q286_raw_pointwise_trigger"],
            "insufficient")
        self.assertIn(
            "Upper bounds",
            rows["Lichtman_2023_Goldbach_upper_bounds"]["mismatch"])

        self.assertEqual(
            rows["Bauer_Wang_2013_binary_AP_large_modulus"][
                "fit_to_q286_raw_pointwise_trigger"],
            "not_promoted")
        self.assertIn(
            "did not verify",
            rows["Bauer_Wang_2013_binary_AP_large_modulus"]["mismatch"])

    def test_required_bridge_shape_is_raw_pointwise(self):
        receipt = self.load_receipt()
        shape = receipt["required_bridge_shape"]

        self.assertEqual(
            shape["quantifier"], "every sufficiently large covered even N")
        self.assertIn("exact signed q286", shape["weight"])
        self.assertEqual(
            shape["scale"], "raw unnormalized log-prime pair sum")
        self.assertIn("must not normalize by T_N",
                      shape["support_boundary"])
        self.assertIn("explicit threshold N0",
                      shape["finite_remainder"])

    def test_decision_keeps_lane_dormant_until_changed_condition(self):
        receipt = self.load_receipt()

        self.assertIn("does not reactivate",
                      receipt["decision"])
        self.assertIn("raw pointwise weighted binary-prime theorem",
                      receipt["decision"])
        self.assertIn("positive-mass theorem",
                      receipt["decision"])
        self.assertEqual(
            receipt["candidate"]["novelty_label"], "new-to-this-task")
        self.assertIn("inspect Bauer-Wang",
                      receipt["candidate"]["smallest_next_action"])


if __name__ == "__main__":
    unittest.main()
