import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderSingleRawBoundTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-single-raw-bound-target.json"
        ).read_text(encoding="utf-8"))

    def test_boundaries_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_single_raw_lower_bound_subsumes_positive_mass")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["single_raw_lower_bound_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["raw_pointwise_estimate_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])

    def test_single_raw_bound_route_is_classified(self):
        receipt = self.load_receipt()
        route = receipt["route_decision"]

        self.assertTrue(route["single_raw_bound_subsumes_positive_mass"])
        self.assertTrue(route["separate_positive_mass_can_sleep_if_raw_bound_proved"])
        self.assertTrue(route["route_is_still_goldbach_strength"])
        self.assertTrue(route["not_a_denominator_shortcut"])
        self.assertIn("Goldbach-strength", receipt["decision"])

    def test_zero_mass_obstruction_is_explicit(self):
        receipt = self.load_receipt()
        target = receipt["theorem_target"]

        self.assertIn("support is empty", target["zero_mass_obstruction"])
        self.assertIn("R_raw(N)=0", target["zero_mass_obstruction"])
        self.assertIn("at least one prime pair",
                      target["strict_central_existence_implication"])

    def test_finite_calibration_is_not_acceptance(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertFalse(finite["finite_evidence_is_acceptance_condition"])
        self.assertEqual(finite["row_count"], 224)
        self.assertEqual(finite["raw_margin_positive_rows"], 224)
        self.assertEqual(finite["raw_domination_failure_targets"], [])
        self.assertEqual(finite["positive_pair_count_rows"], 224)
        self.assertEqual(finite["positive_total_weight_rows"], 224)
        self.assertEqual(finite["zero_pair_count_targets"], [])

    def test_key_horizon_numbers_are_preserved(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]
        tight = finite["tight_raw_margin_row"]
        smallest_pair = finite["smallest_pair_count_row"]

        self.assertEqual(tight["target"], 44168)
        self.assertAlmostEqual(
            tight["raw_pointwise_margin"], 471324043.51697165)
        self.assertEqual(smallest_pair["target"], 24148)
        self.assertEqual(
            smallest_pair["ordered_central_prime_pair_count"], 106)
        self.assertAlmostEqual(
            smallest_pair["strict_central_total_weight"],
            9320.216763448925)


if __name__ == "__main__":
    unittest.main()
