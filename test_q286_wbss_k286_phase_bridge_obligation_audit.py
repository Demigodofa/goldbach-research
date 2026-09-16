import json
import unittest
from pathlib import Path


class Q286WbssK286PhaseBridgeObligationAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-phase-bridge-obligation-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_theorem_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_broad_k286_phase_cancellation_bridge_required")
        self.assertFalse(receipt["broad_phase_envelope_theorem_proved"])
        self.assertFalse(receipt["phase_cancellation_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_phase_diagnostic_values_are_carried_forward(self):
        receipt = self.load_receipt()
        diagnostic = receipt["finite_phase_diagnostic"]

        self.assertFalse(
            diagnostic["finite_evidence_is_acceptance_condition"])
        self.assertEqual(diagnostic["row_count"], 32)
        self.assertEqual(diagnostic["pair_count_per_row"], 30.0)
        self.assertEqual(diagnostic["cover_count_mean_50"], 6.625)
        self.assertEqual(diagnostic["cover_count_mean_75"], 11.9375)
        self.assertEqual(diagnostic["cover_count_mean_90"], 16.875)
        self.assertEqual(diagnostic["cover_count_min_90"], 15.0)
        self.assertEqual(diagnostic["cover_count_max_90"], 19.0)
        self.assertAlmostEqual(
            diagnostic["top_pair_fraction_max"],
            0.16050600038977816,
            places=15)

    def test_logical_bridge_stays_unnormalized_pointwise(self):
        receipt = self.load_receipt()
        bridge = receipt["logical_bridge_boundary"]

        self.assertEqual(
            bridge["active_acceptance_target"],
            "universal pointwise unnormalized adverse-drag inequality")
        self.assertIn("adverse_drag(N) < local_main(N)",
                      bridge["required_universal_statement"])
        self.assertIn("unnormalized", bridge["normalization_boundary"])
        self.assertIn("finite remainder",
                      bridge["finite_remainder_requirement"])

    def test_phase_obligation_excludes_sparse_or_normalized_shortcuts(self):
        receipt = self.load_receipt()
        obligation = receipt["phase_theorem_obligation"]
        not_enough = " ".join(obligation["not_enough"])

        self.assertIn("E_286(N)=sum_p P_p(N)",
                      obligation["signed_pair_sum_form"])
        self.assertIn("B_70(N)+B_130(N)+B_154(N)+B_286(N) < M(N)",
                      obligation["acceptable_k286_subgoal"])
        self.assertIn("A_-(N)=sum_d max(0,-E_d(N)) < M(N)",
                      obligation["acceptable_full_goal"])
        self.assertIn("dominant phase-pair labels", not_enough)
        self.assertIn("normalized L2 premise", not_enough)


if __name__ == "__main__":
    unittest.main()
