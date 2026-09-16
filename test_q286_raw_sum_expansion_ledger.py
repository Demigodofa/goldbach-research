import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/q286-raw-sum-expansion-ledger.json")


class Q286RawSumExpansionLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_proof_boundaries(self):
        self.assertEqual(self.receipt["status"],
                         "LEDGER_q286_raw_sum_expansion")
        self.assertTrue(self.receipt["finite_ledger_only"])
        self.assertTrue(self.receipt["raw_sum_definitions_confirmed"])
        self.assertFalse(self.receipt["l2_logical_bridge_confirmed"])
        self.assertFalse(self.receipt["q286_q46189_combined_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_theorem_ready_statements_do_not_use_mu(self):
        ledger = self.receipt["raw_sum_ledger"]
        theorem_ready = [
            ledger["raw_modulus_error_U_d"]["formula"],
            ledger["raw_witness_W_phi"]["direct_sum"],
            ledger["raw_witness_W_phi"]["decomposition"],
            ledger["raw_adverse_envelope_A_raw_minus"]["formula"],
        ]
        for statement in theorem_ready:
            self.assertNotIn("mu_N", statement)
        self.assertEqual(
            ledger["raw_modulus_error_U_d"]["classification"],
            "theorem_ready_raw_sum",
        )

    def test_zero_mass_does_not_promote_l2_bridge(self):
        logical = self.receipt["logical_implication"]
        l2 = self.receipt["l2_bridge_status"]
        self.assertIn("false 0<0", logical["noncircular_conclusion"])
        self.assertTrue(l2["zero_mass_sanity_confirmed"])
        self.assertFalse(l2["logical_bridge_confirmed"])
        self.assertEqual(l2["classification"],
                         "target_only_not_acceptance_condition")

    def test_adverse_drag_implication_is_explicit(self):
        implication = self.receipt["logical_implication"]["adverse_drag_route"]
        self.assertIn("A_raw_-(N)<L_raw(N)", implication)
        self.assertIn("W_phi(N)=L_raw(N)+sum_d U_d(N)>0", implication)

    def test_q286_q46189_bridge_stays_diagnostic(self):
        bridge = self.receipt["q286_q46189_bridge_read"]
        self.assertFalse(bridge["combined_proof_established"])
        self.assertIn("residual", bridge["bridge_obligation"])
        self.assertEqual(
            bridge["q46189_best_input_feature"]["feature"],
            "missing_count",
        )
        self.assertEqual(
            bridge["q46189_best_matrix_feature"]["feature"],
            "tension_sum",
        )

    def test_finite_evidence_not_acceptance(self):
        summary = self.receipt["finite_calibration_summary"]
        self.assertFalse(summary["finite_evidence_is_acceptance_condition"])
        self.assertTrue(summary["all_checked_raw_gate_gaps_positive"])
        self.assertGreater(summary["row_count"], 0)


if __name__ == "__main__":
    unittest.main()
