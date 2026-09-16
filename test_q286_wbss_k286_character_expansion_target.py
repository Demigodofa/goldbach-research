import json
import unittest
from pathlib import Path


class Q286WbssK286CharacterExpansionTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-character-expansion-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_k286_character_expansion_bridge_unproved")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["k286_pointwise_lower_bound_proved"])
        self.assertFalse(receipt["major_minor_arc_estimate_proved"])
        self.assertFalse(
            receipt["pointwise_centered_error_estimate_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])
        self.assertFalse(receipt["L2_logical_bridge_confirmed"])

    def test_dominant_286_package_is_pinned(self):
        receipt = self.load_receipt()
        bucket = receipt["target_bucket"]

        self.assertEqual(bucket["bucket"], "dominant_286")
        self.assertEqual(bucket["support_label"], "11x13")
        self.assertEqual(bucket["natural_modulus"], 286)
        self.assertEqual(bucket["support_primes"], [11, 13])
        self.assertEqual(bucket["character_count"], 99)
        self.assertEqual(bucket["unit_residue_count"], 120)
        self.assertTrue(bucket["descends_to_natural_modulus"])
        self.assertAlmostEqual(
            bucket["energy_fraction"], 0.70082890257693, places=12)
        self.assertAlmostEqual(
            bucket["allocated_negative_budget_ratio"],
            0.1759037368828583,
            places=12)
        self.assertEqual(
            bucket["required_raw_lower_bound"],
            "K_286(N) >= -0.1759037368828583*P0_a(N)")

    def test_character_set_excludes_principal_term(self):
        receipt = self.load_receipt()
        chars = receipt["character_set"]
        terms = receipt["principal_and_nonprincipal_terms"]

        self.assertIn("nontrivial on 11", chars["notation"])
        self.assertIn("nontrivial on 13", chars["notation"])
        self.assertEqual(chars["count_formula"], "(11-2)*(13-2)=99.")
        self.assertFalse(chars["principal_character_included"])
        self.assertFalse(terms["centered_bucket_principal_term_found"])
        self.assertEqual(terms["nonprincipal_terms_to_control"], 99)
        self.assertIn("No standalone positive principal term",
                      terms["principal_term_status"])

    def test_raw_moment_formula_uses_unnormalized_pointwise_scale(self):
        receipt = self.load_receipt()
        moments = receipt["raw_moments"]
        obligation = receipt["theorem_obligation"]

        self.assertIn("C_chi(N)=sum_{p in I_N",
                      moments["twisted_pair_mass"])
        self.assertIn("U_{a,chi}^{286}",
                      moments["local_uniform_character_mean"])
        self.assertIn("D_chi^P(N)=C_chi(N)-U_{a,chi}^{286}*P0_a(N)",
                      moments["proof_scale_moment"])
        self.assertIn("K_286(N)=sum_{chi in X_286(11x13)}",
                      moments["bucket_sum"])
        self.assertEqual(
            obligation["required_pointwise_inequality"],
            "K_286(N) >= -0.1759037368828583*P0_a(N)")
        self.assertIn("every sufficiently large covered even N",
                      obligation["quantifier"])

    def test_zero_mass_l2_and_collapse_boundaries_are_explicit(self):
        receipt = self.load_receipt()
        check = receipt["zero_mass_and_collapse_check"]
        warning = receipt["principal_and_nonprincipal_terms"][
            "P0_scale_warning"]

        self.assertIn("C_0(N)=0", check["if_T_N_is_zero"])
        self.assertIn("L2 target is not confirmed",
                      check["L2_status"])
        self.assertIn("pointwise before importing T_N>0",
                      check["L2_status"])
        self.assertIn("first proves or assumes T_N>0",
                      check["collapses_if"])
        self.assertIn("C_0(N)-P0_a(N) mismatch", warning)
        self.assertIn("not allowed to divide by or assume T_N>0", warning)

    def test_decision_preserves_unproved_status(self):
        receipt = self.load_receipt()

        self.assertIn("99-character modulus-286 raw lower bound",
                      receipt["decision"])
        self.assertIn("nonfinite, pointwise, unnormalized analytic",
                      receipt["decision"])
        self.assertIn("not a theorem", receipt["status_boundary"])
        self.assertIn("does not confirm L2 as a logical bridge",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
