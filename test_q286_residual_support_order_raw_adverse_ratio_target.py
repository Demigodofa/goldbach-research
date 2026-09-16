import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderRawAdverseRatioTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-raw-adverse-ratio-target.json"
        ).read_text(encoding="utf-8"))

    def test_boundaries_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_raw_adverse_ratio_plus_positive_low_order")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["raw_adverse_ratio_theorem_proved"])
        self.assertFalse(receipt["positive_low_order_theorem_proved"])
        self.assertFalse(receipt["raw_lower_bound_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])

    def test_finite_ratio_calibration_is_stable(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertFalse(finite["finite_evidence_is_acceptance_condition"])
        self.assertEqual(finite["row_count"], 224)
        self.assertEqual(finite["positive_low_order_rows"], 224)
        self.assertEqual(finite["nonpositive_low_order_targets"], [])
        self.assertEqual(finite["zero_adverse_drag_rows"], 124)
        self.assertEqual(finite["nonzero_adverse_drag_rows"], 100)
        self.assertEqual(finite["ratio_less_than_one_rows"], 224)
        self.assertEqual(finite["ratio_not_less_than_one_targets"], [])

    def test_stress_rows_are_preserved(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertEqual(
            finite["smallest_low_order_row"]["target"], 24148)
        self.assertAlmostEqual(
            finite["smallest_low_order_row"]["raw_low_order_base"],
            494408133.6057817)
        self.assertEqual(
            finite["largest_adverse_ratio_row"]["target"], 164926)
        self.assertAlmostEqual(
            finite["largest_adverse_ratio_row"][
                "adverse_drag_ratio_to_low_order"],
            0.13266261119465184)
        self.assertAlmostEqual(
            finite["largest_adverse_ratio_row"]["ratio_slack_to_one"],
            0.8673373888053482)
        self.assertEqual(
            finite["tightest_raw_margin_row"]["target"], 44168)

    def test_ratio_route_requires_positive_low_order_boundary(self):
        receipt = self.load_receipt()
        target = receipt["theorem_target"]
        route = receipt["route_decision"]

        self.assertIn("B_low_raw(N)>0", target["sufficient_conditions"])
        self.assertIn("undefined", target["zero_support_boundary"])
        self.assertTrue(route["ratio_route_is_valid_sufficient_shape"])
        self.assertTrue(route["ratio_route_requires_positive_low_order"])
        self.assertTrue(route["positive_low_order_is_not_a_minor_side_condition"])
        self.assertTrue(route["single_raw_lower_bound_remains_cleaner"])


if __name__ == "__main__":
    unittest.main()
