import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-clearance-logical-bridge-audit.json")


class MobiusMomentSquareDegree5ClearanceLogicalBridgeAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_is_hold_not_proof(self):
        self.assertEqual(
            self.receipt["status"],
            "HOLD_clearance_logical_bridge_not_confirmed")
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["moving_prime_block_theorem_proved"])
        self.assertFalse(self.receipt["clearance_family_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_finite_decomposition_is_confirmed_but_not_acceptance(self):
        finite = self.receipt["finite_evidence"]
        bridge = self.receipt["logical_bridge_classification"]

        self.assertEqual(finite["band_minimum_blocks_checked"], 4)
        self.assertEqual(finite["tight_source_blocks_checked"], 6)
        self.assertTrue(finite["finite_decomposition_confirmed"])
        self.assertAlmostEqual(
            finite["maximum_near_negative_over_middle_far_positive"],
            0.0016400172796714467)
        self.assertTrue(bridge["non_circular_theorem_shape_defined"])
        self.assertFalse(bridge["logical_bridge_confirmed"])
        self.assertFalse(bridge["finite_evidence_is_acceptance_condition"])

    def test_false_all_negative_near_shortcut_is_rejected(self):
        bridge = self.receipt["logical_bridge_classification"]
        invalid = self.receipt["invalid_substitutes"]

        self.assertTrue(bridge["false_all_negative_near_shortcut_confirmed"])
        self.assertIn("the false all-negative-near shortcut", invalid)
        self.assertIn("finite clearance ratios", invalid)

    def test_pointwise_target_is_unnormalized(self):
        target = self.receipt["pointwise_unnormalized_target"]

        self.assertIn("A=int((M**(1/.59))**.41)",
                      target["source_parameters"])
        self.assertIn("A_near", target["margin_components"])
        self.assertIn("G_middle_far", target["margin_components"])
        self.assertIn("G_middle_far(M,p,ell) > A_near(M,p,ell)",
                      target["sufficient_pointwise_inequality"])

    def test_required_independent_obligations_are_pinned(self):
        obligations = {
            row["id"]: row
            for row in self.receipt["required_independent_obligations"]
        }

        self.assertEqual(
            set(obligations),
            {
                "moving_prime_sigma_coverage",
                "near_adverse_upper_bound",
                "middle_far_lower_bound",
                "comparison_margin",
                "finite_remainder",
            })
        self.assertIn("without using total margin positivity",
                      obligations["near_adverse_upper_bound"]["statement"])
        self.assertIn("without reusing the target positivity claim",
                      obligations["middle_far_lower_bound"]["statement"])

    def test_next_action_targets_exception_not_more_scan(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"],
            "independent near-vs-middlefar denominator bounds")
        self.assertIn("M=229,p=379", action["smallest_next_test"])
        self.assertIn("Q=46189", action["smallest_next_test"])
        self.assertEqual(action["novelty_label"], "new-to-this-task")


if __name__ == "__main__":
    unittest.main()
