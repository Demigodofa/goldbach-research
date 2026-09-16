import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderPositiveLowOrderObligationTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-positive-low-order-obligation.json"
        ).read_text(encoding="utf-8"))

    def test_boundaries_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_positive_low_order_is_support_strength")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["positive_low_order_theorem_proved"])
        self.assertFalse(receipt["normalized_low_order_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["raw_adverse_ratio_theorem_proved"])
        self.assertFalse(receipt["raw_lower_bound_theorem_proved"])

    def test_identity_records_zero_support_boundary(self):
        receipt = self.load_receipt()
        identity = receipt["identity"]

        self.assertIn("b_low_norm", identity["raw_low_order_base"])
        self.assertTrue(identity["principal_mean_positive_on_current_context"])
        self.assertIn("B_low_raw(N)=0",
                      identity["zero_support_implication"])

    def test_finite_low_order_calibration_is_stable(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertFalse(finite["finite_evidence_is_acceptance_condition"])
        self.assertEqual(finite["row_count"], 224)
        self.assertEqual(finite["positive_raw_low_order_rows"], 224)
        self.assertEqual(finite["nonpositive_raw_low_order_targets"], [])
        self.assertEqual(finite["positive_normalized_low_order_rows"], 224)
        self.assertEqual(
            finite["nonpositive_normalized_low_order_targets"], [])

    def test_key_minimum_rows_are_preserved(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertEqual(
            finite["smallest_raw_low_order_row"]["target"], 24148)
        self.assertAlmostEqual(
            finite["smallest_raw_low_order_row"]["raw_low_order_base"],
            494408133.6057817)
        self.assertEqual(
            finite["smallest_normalized_low_order_row"]["target"], 255016)
        self.assertAlmostEqual(
            finite["smallest_normalized_low_order_row"][
                "normalized_low_order_base"],
            0.2943409774960611)
        self.assertEqual(
            finite["smallest_total_weight_row"]["target"], 24148)

    def test_route_decision_prefers_direct_raw_bound(self):
        receipt = self.load_receipt()
        route = receipt["route_decision"]

        self.assertFalse(route["positive_low_order_can_replace_positive_mass"])
        self.assertTrue(route["direct_raw_low_order_positive_subsumes_support"])
        self.assertTrue(
            route["normalized_low_order_positive_still_needs_positive_mass"])
        self.assertTrue(route["split_ratio_route_has_two_goldbach_strength_inputs"])
        self.assertTrue(route["single_raw_lower_bound_remains_preferred"])


if __name__ == "__main__":
    unittest.main()
