import json
import unittest
from pathlib import Path


class Q286WbssSignedWeightProofEngineSleepHoldTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-signed-weight-proof-engine-sleep-hold.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_lane_sleep_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SLEEP_q286_signed_weight_proof_engine_until_raw_estimate")
        self.assertFalse(
            receipt["signed_weight_major_arc_estimate_proved"])
        self.assertFalse(receipt["raw_weighted_witness_theorem_proved"])
        self.assertFalse(receipt["active_character_moment_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("Lane-level sleep/HOLD only",
                      receipt["status_boundary"])

    def test_sleep_scope_preserves_useful_components(self):
        receipt = self.load_receipt()
        scope = receipt["sleep_scope"]

        self.assertEqual(
            scope["attention_state"], "dormant_until_changed_condition")
        self.assertEqual(
            scope["epistemic_state"],
            "supported_HOLD_for_exact_conjunction")
        self.assertIn("raw direct W_phi(N)>0 theorem target",
                      scope["not_slept"])
        self.assertIn("K_286 finite falsifier/calibration lane",
                      scope["not_slept"])
        self.assertIn("q286 as proof engine via local-factor positivity",
                      scope["sleep_exact_family"])

    def test_blocked_conjunctions_are_pinned(self):
        receipt = self.load_receipt()
        blocked = {
            row["id"]: row for row in receipt["blocked_conjunctions"]
        }

        self.assertEqual(len(blocked), 4)
        self.assertIn("support_only_single_weight_positive_floor", blocked)
        self.assertIn("normalized_l2_as_bridge", blocked)
        self.assertIn("principal_local_factor_as_independent_support",
                      blocked)
        self.assertIn("named_external_signed_region_bridge", blocked)
        self.assertTrue(all(row["blocked"] for row in blocked.values()))
        self.assertIn("T_N*M(a)",
                      blocked[
                          "principal_local_factor_as_independent_support"][
                              "evidence"])

    def test_preserved_component_numbers_are_pinned(self):
        receipt = self.load_receipt()
        components = receipt["preserved_components"]

        positive = components["positive_local_factors"]
        self.assertEqual(positive["state"], "supported_component_not_bridge")
        self.assertAlmostEqual(
            positive["minimum_M"], 0.6039353780830684, places=15)
        self.assertAlmostEqual(
            positive["maximum_M"], 1.5716524655081634, places=15)

        shape = components["signed_shape_margin"]
        self.assertEqual(
            shape["state"], "supported_component_not_distribution_theorem")
        self.assertAlmostEqual(
            shape["shape_threshold_minimum"],
            0.48729403831397616,
            places=15)
        self.assertAlmostEqual(
            shape["minimum_local_uniform_shape_margin"],
            0.10534041937277128,
            places=15)

        k286 = components["k286_quarter_residual_calibration"]
        self.assertEqual(k286["state"], "finite_falsifier_calibration")
        self.assertEqual(k286["row_count"], 560)
        self.assertAlmostEqual(
            k286["max_companion_residual_fraction"],
            0.24495753331096648,
            places=15)

    def test_reactivation_triggers_are_raw_or_changed_condition(self):
        receipt = self.load_receipt()
        triggers = {
            row["trigger"]: row for row in receipt["reactivation_triggers"]
        }

        self.assertEqual(len(triggers), 4)
        self.assertIn("raw_pointwise_weighted_binary_prime_theorem",
                      triggers)
        self.assertIn("materially_new_signed_weight", triggers)
        self.assertIn("raw_moment_theorem_for_active_characters", triggers)
        self.assertIn("explicit_positive_mass_theorem_labeled_as_such",
                      triggers)
        self.assertIn("raw pointwise", receipt["decision"])
        self.assertIn("finite diagnostics",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
