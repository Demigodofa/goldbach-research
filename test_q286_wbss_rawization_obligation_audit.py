import json
import unittest
from pathlib import Path


class Q286WbssRawizationObligationAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-rawization-obligation-audit.json"
        ).read_text(encoding="utf-8"))

    def test_pointwise_gate_is_classified_as_mass_conditional(self):
        receipt = self.load_receipt()
        audit = receipt["mass_boundary_audit"]

        self.assertTrue(audit["uses_normalized_actual_measure_mu_N"])
        self.assertTrue(audit["local_main_has_no_pair_count_factor"])
        self.assertTrue(audit["finite_zero_mass_check_passed"])
        self.assertEqual(audit["finite_zero_pair_count"], 0)
        self.assertEqual(audit["finite_zero_actual_mass_count"], 0)
        self.assertIn("does not supply a universal positive-mass theorem",
                      audit["logical_consequence"])

    def test_corrected_paths_separate_raw_and_two_theorem_routes(self):
        receipt = self.load_receipt()
        paths = receipt["corrected_theorem_paths"]

        self.assertEqual(paths["path_A_raw_witness"]["status"],
                         "preferred_clean_bridge_but_unproved")
        self.assertIn("W_Phi(N)>0",
                      paths["path_A_raw_witness"]["statement"])
        self.assertEqual(
            paths["path_B_positive_mass_plus_distribution"]["status"],
            "two_theorem_bridge_unproved")
        self.assertIn(
            "T_N>0",
            paths["path_B_positive_mass_plus_distribution"]["statement"])

    def test_finite_calibration_is_not_acceptance(self):
        receipt = self.load_receipt()
        finite = receipt["finite_calibration"]

        self.assertFalse(finite["finite_evidence_is_acceptance_condition"])
        self.assertEqual(finite["row_count"], 348)
        self.assertEqual(finite["positive_actual_formula_rows"], 348)
        self.assertAlmostEqual(
            finite["adverse_drag_ratio_summary"]["maximum"],
            0.23148438379145228,
            places=12)

    def test_no_theorem_or_goldbach_promotion(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["raw_witness_theorem_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])


if __name__ == "__main__":
    unittest.main()
