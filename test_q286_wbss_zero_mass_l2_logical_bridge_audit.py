import json
import unittest
from pathlib import Path


class Q286WbssZeroMassL2LogicalBridgeAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-zero-mass-l2-logical-bridge-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_l2_logical_bridge_not_confirmed")
        self.assertFalse(receipt["aggregate_l2_theorem_proved"])
        self.assertFalse(
            receipt["raw_twisted_binary_prime_theorem_proved"])
        self.assertFalse(
            receipt["signed_weight_circle_method_estimate_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_zero_mass_arithmetic_sanity_is_checked_scope_only(self):
        receipt = self.load_receipt()
        zero = receipt["zero_mass_check"]

        self.assertEqual(zero["checked_row_count"], 348)
        self.assertEqual(zero["zero_pair_count"], 0)
        self.assertEqual(zero["zero_actual_mass_count"], 0)
        self.assertEqual(zero["nonunit_actual_mass_sum_count"], 0)
        self.assertEqual(zero["nonunit_uniform_mass_sum_count"], 0)
        self.assertTrue(
            zero["arithmetic_sanity_confirmed_on_checked_rows"])
        self.assertIn("finite checked rows only", zero["scope"])

    def test_l2_bridge_classification_is_pinned(self):
        receipt = self.load_receipt()
        classification = receipt["l2_bridge_classification"]

        self.assertTrue(
            classification[
                "raw_strict_aggregate_l2_shape_is_noncircular"])
        self.assertFalse(classification["logical_bridge_confirmed"])
        self.assertEqual(
            classification["current_hold"],
            "HOLD_for_strict_raw_binary_pair_estimate")
        self.assertIn("No pointwise raw twisted binary-prime moment theorem",
                      classification["reason_bridge_not_confirmed"])

    def test_observed_l2_failures_are_pinned(self):
        receipt = self.load_receipt()
        failures = receipt["observed_l2_failures"]

        self.assertEqual(failures["row_count"], 348)
        self.assertEqual(
            failures["global_min_cap_exceeding_row_count"], 301)
        self.assertEqual(failures["row_local_cap_exceeding_row_count"], 120)
        self.assertEqual(failures["worst_row_local_ratio_target"], 1089544)
        self.assertAlmostEqual(
            failures["worst_row_local_ratio"],
            1.5570989543984672,
            places=15)
        self.assertAlmostEqual(
            failures["worst_row_observed_aggregate_l2"],
            0.20982859176041493,
            places=15)
        self.assertAlmostEqual(
            failures["worst_row_local_l2_cap"],
            0.13475610600578378,
            places=15)

    def test_acceptance_condition_rejects_finite_substitutes(self):
        receipt = self.load_receipt()
        acceptance = receipt["acceptance_condition"]
        target = receipt["coefficient_l2_target"]

        self.assertFalse(acceptance["finite_evidence_is_acceptance_condition"])
        self.assertIn("universal pointwise unnormalized estimate",
                      acceptance["required_for_acceptance"])
        self.assertIn("checked-row zero-mass sanity",
                      acceptance["invalid_substitutes"])
        self.assertAlmostEqual(
            target["aggregate_coefficient_l2"],
            5.525106448699807,
            places=15)
        self.assertAlmostEqual(
            target["global_minimum_local_main_cap"],
            0.10930746469603118,
            places=15)
        self.assertIn("No aggregate L2 theorem",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
