import json
import unittest
from pathlib import Path


class Q286WbssLogicBridgeGateAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-logic-bridge-gate-audit.json"
        ).read_text(encoding="utf-8"))

    def test_zero_mass_check_is_finite_not_a_bridge(self):
        receipt = self.load_receipt()
        zero = receipt["zero_mass_gate"]

        self.assertTrue(zero["finite_zero_mass_check_passed"])
        self.assertEqual(zero["checked_rows"], 348)
        self.assertEqual(zero["zero_pair_count"], 0)
        self.assertEqual(zero["zero_actual_mass_count"], 0)
        self.assertIn("does not prove positivity", zero["bridge_consequence"])

    def test_normalized_l2_is_not_promoted(self):
        receipt = self.load_receipt()
        l2 = receipt["normalized_l2_gate"]

        self.assertTrue(l2["valid_conditional_distribution_shape"])
        self.assertTrue(l2["non_circular_only_as_external_arithmetic_premise"])
        self.assertFalse(l2["confirmed_by_current_work"])
        self.assertFalse(l2["proves_strict_central_existence"])
        self.assertEqual(l2["wbss_row_local_l2_cap_violations"], 120)
        self.assertEqual(l2["wbss_global_minimum_l2_cap_violations"], 301)
        self.assertEqual(l2["largest_row_local_ratio_target"], 1089544)
        self.assertAlmostEqual(l2["largest_row_local_ratio"],
                               1.5570989543984672)

    def test_unnormalized_pointwise_gate_is_active_target(self):
        receipt = self.load_receipt()
        pointwise = receipt["unnormalized_pointwise_gate"]
        decision = receipt["route_decision"]

        self.assertFalse(pointwise["finite_evidence_is_acceptance_condition"])
        self.assertIn("adverse_drag(N) < local_main(N)",
                      pointwise["required_universal_statement"])
        self.assertIn("unnormalized", pointwise["normalization_boundary"])
        self.assertEqual(
            decision["active_acceptance_target"],
            "universal pointwise unnormalized adverse-drag inequality")

    def test_no_theorem_or_goldbach_promotion(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["l2_discrepancy_theorem_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(
            receipt["strict_central_prime_pair_existence_proved"])
        self.assertTrue(receipt["universal_bound_open"])


if __name__ == "__main__":
    unittest.main()
