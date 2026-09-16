import json
import unittest
from pathlib import Path

from tools.build_q286_residual_support_order_raw_bound_phase_space import (
    HTML_OUT,
    OUT,
    build_view_model,
    script_json,
)


class Q286ResidualSupportOrderRawBoundPhaseSpaceTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(OUT.read_text(encoding="utf-8"))

    def test_boundaries_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "CALIBRATION_raw_bound_phase_space_stress_locator")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["raw_lower_bound_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["raw_pointwise_estimate_proved"])
        self.assertFalse(receipt["finite_horizon"][
            "finite_evidence_is_acceptance_condition"])

    def test_phase_space_schema_matches_raw_theorem_target(self):
        receipt = self.load_receipt()
        schema = receipt["visual_schema"]

        self.assertEqual(schema["x"], "log(target)")
        self.assertEqual(
            schema["y"], "ordered strict-central prime-pair count")
        self.assertEqual(schema["z_default"], "raw_pointwise_margin")
        self.assertEqual(schema["color"], "target_mod_286")
        self.assertIn("distance from failure", schema["brightness"])

    def test_finite_horizon_and_stress_rows_are_stable(self):
        receipt = self.load_receipt()
        horizon = receipt["finite_horizon"]
        stress = receipt["stress_rows"]

        self.assertEqual(horizon["row_count"], 224)
        self.assertEqual(horizon["positive_raw_margin_rows"], 224)
        self.assertEqual(horizon["raw_domination_failure_targets"], [])
        self.assertEqual(horizon["negative_high_order_tail_rows"], 100)
        self.assertEqual(horizon["nonnegative_high_order_tail_rows"], 124)
        self.assertEqual(
            stress["tightest_raw_margin_row"]["target"], 44168)
        self.assertAlmostEqual(
            stress["tightest_raw_margin_row"]["raw_pointwise_margin"],
            471324043.51697165)
        self.assertEqual(
            stress["largest_adverse_ratio_row"]["target"], 164926)
        self.assertAlmostEqual(
            stress["largest_adverse_ratio_row"][
                "adverse_drag_ratio_to_low_order"],
            0.13266261119465184)
        self.assertEqual(
            stress["smallest_pair_count_row"]["target"], 24148)

    def test_shape_correlations_are_recorded_as_finite_diagnostics(self):
        receipt = self.load_receipt()
        shape = receipt["shape_diagnostics"]

        self.assertAlmostEqual(
            shape["correlation_log_target_to_log_raw_margin"],
            0.9456990848108981)
        self.assertAlmostEqual(
            shape["correlation_pair_count_to_log_raw_margin"],
            0.8915845948837736)
        self.assertAlmostEqual(
            shape["correlation_log_total_weight_to_log_raw_margin"],
            0.980275224825557)
        self.assertIn("finite horizon", shape["interpretation"])

    def test_html_view_model_preserves_clickable_row_details(self):
        receipt = self.load_receipt()
        view = build_view_model(receipt)

        self.assertEqual(len(view["rows"]), 224)
        tight = next(row for row in view["rows"] if row["target"] == 44168)
        self.assertEqual(tight["residue286"], 124)
        self.assertEqual(tight["pairCount"], 196)
        self.assertAlmostEqual(tight["rawMargin"], 471324043.51697165)
        self.assertIn("raw_low_order_base", tight["detail"])
        encoded = script_json(view)
        self.assertIn('"target": 44168', encoded)
        self.assertNotIn("&quot;", encoded)
        self.assertTrue(HTML_OUT.exists())


if __name__ == "__main__":
    unittest.main()
