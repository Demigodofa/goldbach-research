import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/q286-raw-adverse-envelope-definition-audit.json")


class Q286RawAdverseEnvelopeDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q286_raw_adverse_envelope_definition")
        self.assertTrue(self.receipt["finite_definition_audit_only"])
        self.assertFalse(self.receipt["positive_mass_theorem_proved"])
        self.assertFalse(self.receipt["raw_adverse_envelope_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_distinguishes_conditional_and_raw_states(self):
        states = self.receipt["three_bridge_states"]
        self.assertEqual(
            states["conditional_distribution_state"]["status"],
            "not_a_goldbach_bridge_by_itself",
        )
        self.assertEqual(
            states["formal_raw_strict_state"]["status"],
            "noncircular_theorem_shape_but_unproved",
        )
        self.assertEqual(
            states["theorem_ready_raw_sum_state"]["status"],
            "required_next_theorem_form",
        )

    def test_classifies_mu_and_raw_errors(self):
        definitions = self.receipt["definitions_audit"]
        self.assertEqual(
            definitions["normalized_mu_N"]["classification"],
            "conditional_only",
        )
        self.assertEqual(
            definitions["raw_projected_errors_U_d"]["classification"],
            "theorem_ready_only_when_defined_directly",
        )
        self.assertEqual(
            definitions["raw_adverse_envelope_A_raw_minus"]["classification"],
            "noncircular_strict_target_unproved",
        )

    def test_finite_calibration_stays_non_acceptance(self):
        summary = self.receipt["finite_calibration_summary"]
        self.assertFalse(summary["finite_evidence_is_acceptance_condition"])
        self.assertTrue(summary["all_checked_raw_gate_gaps_positive"])
        self.assertGreater(summary["row_count"], 0)
        self.assertGreater(summary["minimum_raw_adverse_gate_gap"], 0)

    def test_next_action_is_raw_sum_expansion(self):
        decision = self.receipt["route_decision"]
        self.assertTrue(
            decision["q286_raw_adverse_envelope_noncircular_as_statement"])
        self.assertFalse(decision["q286_raw_adverse_envelope_theorem_proved"])
        self.assertIn("raw-sum expansion ledger", decision["next_action"])


if __name__ == "__main__":
    unittest.main()
