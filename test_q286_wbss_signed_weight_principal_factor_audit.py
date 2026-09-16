import json
import unittest
from pathlib import Path


class Q286WbssSignedWeightPrincipalFactorAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-signed-weight-principal-factor-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_signed_weight_principal_factor_TN_dependent")
        self.assertFalse(
            receipt["signed_weight_major_arc_estimate_proved"])
        self.assertFalse(receipt["raw_weighted_witness_theorem_proved"])
        self.assertFalse(
            receipt["signed_negative_region_distribution_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_principal_factorization_is_tn_dependent(self):
        receipt = self.load_receipt()
        factorization = receipt["principal_factorization"]

        self.assertIn("T_N*M(a)",
                      factorization["signed_weight_principal_term"])
        self.assertIn("Principal_q286(N)=0",
                      factorization["if_T_N_zero"])
        self.assertFalse(
            factorization["independent_principal_surplus_found"])
        self.assertIn("not just a positive local factor",
                      factorization["support_creation_requires"])

    def test_local_factor_summary_is_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["local_factor_summary"]
        local = summary["local_factor_M_summary"]
        local_minus_one = summary["local_factor_M_minus_one_summary"]

        self.assertEqual(summary["even_target_residue_count"], 5005)
        self.assertEqual(summary["positive_principal_factor_count"], 5005)
        self.assertEqual(summary["nonpositive_principal_factor_count"], 0)
        self.assertAlmostEqual(
            local["minimum"], 0.6039353780830684, places=15)
        self.assertAlmostEqual(local["mean"], 1.0, places=15)
        self.assertAlmostEqual(
            local["maximum"], 1.5716524655081634, places=15)
        self.assertAlmostEqual(
            local_minus_one["minimum"], -0.3960646219169316, places=15)
        self.assertAlmostEqual(
            local_minus_one["maximum"], 0.5716524655081634, places=15)

    def test_extreme_rows_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["local_factor_summary"]
        obstruction = receipt["signed_weight_obstruction_summary"]

        min_local = summary["minimum_local_factor_row"]
        self.assertEqual(min_local["target_residue"], 4124)
        self.assertEqual(min_local["target_mod_286"], 120)
        self.assertAlmostEqual(
            min_local["local_uniform_expectation"],
            0.6039353780830684,
            places=15)

        max_local = summary["maximum_local_factor_row"]
        self.assertEqual(max_local["target_residue"], 8856)
        self.assertEqual(max_local["target_mod_286"], 276)
        self.assertAlmostEqual(
            max_local["local_uniform_expectation"],
            1.5716524655081634,
            places=15)

        largest_negative = obstruction["largest_negative_fraction_row"]
        self.assertEqual(largest_negative["target_residue"], 1146)
        self.assertAlmostEqual(
            largest_negative["negative_weight_fraction"],
            0.47205387205387206,
            places=15)

        tight_shape = obstruction["tightest_shape_margin_row"]
        self.assertEqual(tight_shape["target_residue"], 3144)
        self.assertAlmostEqual(
            tight_shape["uniform_margin_to_shape_threshold"],
            0.10534041937277128,
            places=15)

    def test_collapse_classifier_boundary_is_pinned(self):
        receipt = self.load_receipt()
        obstruction = receipt["signed_weight_obstruction_summary"]
        classifier = receipt["collapse_classifier"]

        self.assertEqual(
            obstruction["rows_with_negative_admissible_weight"], 5005)
        self.assertEqual(
            obstruction["rows_with_pointwise_positive_floor"], 0)
        self.assertEqual(
            obstruction["local_uniform_shape_threshold_pass_count"], 5005)
        self.assertEqual(
            obstruction["local_uniform_robust_threshold_pass_count"], 0)
        self.assertIn("principal local-factor algebra alone is conditional",
                      classifier["current_classification"])
        self.assertIn("No signed-weight major/minor arc estimate",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
