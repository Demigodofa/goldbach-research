import json
import unittest
from pathlib import Path


class PostQ286ProofEngineTriageTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/post-q286-proof-engine-triage.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_selects_engine_without_claiming_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_mobius_incomplete_prime_row_covariance_after_q286_sleep")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["q286_reactivated"])
        self.assertFalse(receipt["mobius_covariance_theorem_proved"])
        self.assertFalse(receipt["source_theorem_directly_applies"])
        self.assertIn("unnormalized analytical estimate",
                      receipt["universal_pointwise_acceptance_condition"])

    def test_q286_is_left_as_reservoir(self):
        receipt = self.load_receipt()
        state = receipt["q286_state"]

        self.assertEqual(
            state["active_character_status"],
            "SLEEP_active_character_route_until_independent_raw_theorem_or_new_engine")
        self.assertEqual(
            state["signed_weight_sleep_status"],
            "SLEEP_q286_signed_weight_proof_engine_until_raw_estimate")
        self.assertIn("structured reservoir", state["decision"])
        triggers = {
            item["trigger"] for item in state["reactivation_triggers"]
        }
        self.assertIn("raw_pointwise_weighted_binary_prime_theorem", triggers)
        self.assertIn("materially_new_signed_weight", triggers)

    def test_mobius_target_has_exact_threshold_and_unpaid_block(self):
        receipt = self.load_receipt()
        target = receipt["selected_non_q286_target"]
        paid = target["known_paid_part"]
        unpaid = target["first_unpaid_balanced_block_probe"]

        self.assertEqual(target["name"], "Mobius incomplete prime-row covariance")
        self.assertEqual(
            target["role"], "next_analytical_proof_engine_candidate")
        self.assertEqual(
            paid["paid_length_threshold"]["fraction"], "1499/2000")
        self.assertEqual(paid["paid_length_threshold"]["decimal"], 0.7495)
        self.assertTrue(paid["short_blocks_paid_uniformly_in_location"])
        self.assertTrue(paid["long_blocks_require_arithmetic_input"])
        self.assertEqual(unpaid["block_length"]["fraction"], "3/4")
        self.assertEqual(unpaid["collision_exponent"]["fraction"], "3/2")
        self.assertFalse(unpaid["factor_by_factor_route_proves_block"])
        self.assertTrue(unpaid["signed_bilinear_input_still_required"])

    def test_existing_source_gates_do_not_close_selected_target(self):
        receipt = self.load_receipt()
        target = receipt["selected_non_q286_target"]
        source_gate = target["balanced_source_gate_at_y_3_4_alpha_1_2"]
        rebalance = target["prime_exponent_rebalance_gate_at_mu_59_100"]

        self.assertGreater(
            source_gate["ps_1_3_excess_over_parseval"]["decimal"], 0.4)
        self.assertFalse(source_gate["wright_2_2_upper_range_possible"])
        self.assertFalse(rebalance["wright_possible_for_some_factor_scale"])
        self.assertFalse(rebalance["classical_bv_with_small_divisor"])
        self.assertIsNone(target["wright_factor_range_at_mu_59_100"])

    def test_route_decision_rejects_more_finite_q286_fitting(self):
        receipt = self.load_receipt()
        decision = receipt["route_decision"]

        self.assertEqual(decision["active_next_engine"],
                         "mobius_incomplete_prime_row_covariance")
        self.assertIn("q286 componentwise finite envelopes",
                      decision["sleep_or_reservoir"])
        self.assertIn("should not tighten .125/.126/.13",
                      decision["why_this_changes_next_action"])


if __name__ == "__main__":
    unittest.main()
