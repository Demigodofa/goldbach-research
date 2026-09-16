import json
import unittest
from pathlib import Path


class Q286WbssMajorArcLocalFactorCollapseAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-major-arc-local-factor-collapse-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_classifier_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "LOCAL_FACTOR_principal_term_is_T_N_dependent_"
            "centered_error_open")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["major_minor_arc_estimate_proved"])
        self.assertFalse(
            receipt["pointwise_centered_error_estimate_proved"])
        self.assertFalse(
            receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_exact_decomposition_mentions_tn_dependent_principal_term(self):
        receipt = self.load_receipt()
        decomposition = receipt["exact_local_factor_decomposition"]

        self.assertIn("A_a={u in U_10010", decomposition[
            "admissible_support"])
        self.assertIn("T_N=sum", decomposition["total_mass"])
        self.assertIn("m_a=|A_a|^-1", decomposition["local_mean"])
        self.assertIn("m_a*T_N", decomposition["identity"])
        self.assertIn("W_phi(N)=0", decomposition["zero_mass_behavior"])

    def test_local_factor_numbers_are_pinned(self):
        receipt = self.load_receipt()
        evidence = receipt["local_factor_evidence"]

        self.assertEqual(evidence["even_target_residue_count"], 5005)
        self.assertTrue(evidence["all_local_means_positive"])
        self.assertEqual(evidence["nonpositive_local_main_term_count"], 0)
        self.assertAlmostEqual(
            evidence["local_mean_ratio_minimum"],
            0.6039353780830684,
            places=12)
        self.assertAlmostEqual(
            evidence["local_mean_ratio_maximum"],
            1.5716524655081636,
            places=12)
        self.assertEqual(evidence["weakest_target_residue"], 4124)

    def test_centered_burden_descends_to_lower_moduli(self):
        receipt = self.load_receipt()
        burden = receipt["centered_error_burden"]

        self.assertFalse(burden["full_modulus_10010_support_present"])
        self.assertTrue(
            burden["all_nonzero_supports_descend_to_lower_moduli"])
        self.assertAlmostEqual(
            burden["dominant_99_percent_energy_fraction"],
            0.9960328792226287,
            places=12)
        self.assertEqual(
            [row["natural_modulus"] for row in burden["dominant_supports"]],
            [286, 154, 70])

    def test_sign_indefiniteness_blocks_minorant_shortcut(self):
        receipt = self.load_receipt()
        guard = receipt["sign_indefiniteness_guard"]

        self.assertEqual(
            guard["single_weight_floor_status"],
            "FALSIFIER_pointwise_positive_single_weight_floor")
        self.assertEqual(guard["rows_with_negative_admissible_weight"], 5005)
        self.assertEqual(guard["rows_with_pointwise_positive_floor"], 0)
        self.assertIn("not a coefficientwise minorant", guard["meaning"])

    def test_classifier_separates_survival_from_collapse(self):
        receipt = self.load_receipt()
        classifier = receipt["major_arc_classifier"]

        self.assertFalse(classifier["independent_q286_source_term_found"])
        self.assertIn("m_a times the ordinary strict-central",
                      classifier["principal_term_shape"])
        self.assertIn("inside that same argument", classifier["survives_if"])
        self.assertIn("first imports or assumes T_N>0",
                      classifier["collapses_if"])
        self.assertIn("not an independent q286 source term",
                      receipt["decision"])
        self.assertIn("not a theorem", receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
