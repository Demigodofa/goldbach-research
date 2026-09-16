import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderPositiveMassObligationTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-positive-mass-obligation.json"
        ).read_text(encoding="utf-8"))

    def test_boundaries_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_positive_mass_is_strict_central_existence_obligation")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["strict_central_existence_theorem_proved"])
        self.assertFalse(receipt["raw_pointwise_estimate_proved"])

    def test_finite_horizon_has_positive_mass(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertEqual(finite["row_count"], 224)
        self.assertEqual(finite["positive_pair_count_rows"], 224)
        self.assertEqual(finite["positive_total_weight_rows"], 224)
        self.assertEqual(finite["zero_pair_count_targets"], [])
        self.assertEqual(finite["zero_or_negative_weight_targets"], [])

    def test_pair_count_and_weight_equivalence_holds_on_rows(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertEqual(finite["positive_weight_zero_pair_count_targets"], [])
        self.assertEqual(finite["positive_pair_zero_weight_targets"], [])

    def test_smallest_row_is_preserved(self):
        receipt = self.load_receipt()
        row = receipt["finite_calibration"]["smallest_pair_count_row"]

        self.assertEqual(row["target"], 24148)
        self.assertEqual(row["ordered_central_prime_pair_count"], 106)
        self.assertAlmostEqual(
            row["strict_central_total_weight"],
            9320.216763448925)

    def test_denominator_is_not_demoted_to_minor_lemma(self):
        receipt = self.load_receipt()
        route = receipt["route_decision"]

        self.assertTrue(route["separate_positive_mass_lemma_is_goldbach_strength"])
        self.assertTrue(route["raw_inequality_route_avoids_normalized_division"])
        self.assertIn("strict-central prime pair exists",
                      receipt["theorem_obligation"]["equivalence"])


if __name__ == "__main__":
    unittest.main()
