import json
import unittest
from pathlib import Path


class Q286WbssAdverseDragVsDirectWitnessRouteAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-adverse-drag-vs-direct-witness-route-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_theorem_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["direct_signed_witness_theorem_proved"])
        self.assertFalse(
            receipt[
                "fixed_modulus_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("not an equivalent restatement",
                      receipt["logical_relations"][
                          "direct_witness_does_not_imply_adverse_drag"])

    def test_calibration_set_stays_positive_without_helpful_terms(self):
        receipt = self.load_receipt()
        summary = receipt["finite_route_comparison"]["summary"]

        self.assertEqual(summary["row_count"], 348)
        self.assertEqual(summary["target_minimum"], 1036248)
        self.assertEqual(summary["target_maximum"], 1155862)
        self.assertEqual(summary["direct_witness_positive_count"], 348)
        self.assertEqual(summary["adverse_only_witness_positive_count"], 348)
        self.assertEqual(
            summary["positive_help_needed_for_direct_positivity_count"], 0)

    def test_adverse_drag_route_is_stricter_but_not_wildly_over_tight(self):
        receipt = self.load_receipt()
        summary = receipt["finite_route_comparison"]["summary"]

        fraction = summary["adverse_only_fraction_of_direct_summary"]
        help_fraction = summary["positive_help_fraction_of_direct_summary"]

        self.assertAlmostEqual(fraction["minimum"], 0.7368071926156354)
        self.assertAlmostEqual(fraction["mean"], 0.9335996319912551)
        self.assertLess(fraction["minimum"], 1.0)
        self.assertAlmostEqual(help_fraction["maximum"], 0.2631928073843646)

    def test_largest_route_cost_row_is_recorded(self):
        receipt = self.load_receipt()
        row = receipt["finite_route_comparison"]["summary"][
            "largest_positive_help_fraction_row"]

        self.assertEqual(row["target"], 1098236)
        self.assertAlmostEqual(
            row["adverse_only_fraction_of_direct_witness"],
            0.7368071926156354)
        self.assertAlmostEqual(
            row["positive_help_fraction_of_direct_witness"],
            0.2631928073843646)


if __name__ == "__main__":
    unittest.main()
