import json
import unittest
from pathlib import Path


class Q286WbssRawCharacterExpansionTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-raw-character-expansion-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_raw_character_expanded_q286_WBSS_theorem")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["raw_character_moment_theorem_proved"])
        self.assertFalse(receipt["strict_raw_gap_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_raw_definitions_are_unnormalized(self):
        receipt = self.load_receipt()
        definitions = receipt["raw_character_definitions"]

        self.assertIn("T_N=sum", definitions["central_mass"])
        self.assertIn("Delta_raw", definitions["raw_projection_delta"])
        self.assertIn("T_N*U", definitions["raw_projection_delta"])
        self.assertIn("D_raw", definitions["raw_character_moment"])
        self.assertIn("W_phi(N)=T_N*M(a)", definitions["raw_witness"])
        self.assertIn("G_raw(N)=T_N*M(a)", definitions["strict_raw_gap"])

    def test_l2_shape_is_strict_and_non_circular(self):
        receipt = self.load_receipt()
        aggregate_l2 = receipt["sufficient_raw_theorem_shapes"][
            "aggregate_L2"]

        self.assertTrue(aggregate_l2["non_circular"])
        self.assertIn("< T_N*M(a)", aggregate_l2["statement"])
        self.assertIn("strict inequality fails", aggregate_l2["why"])
        self.assertAlmostEqual(
            aggregate_l2["C2"],
            5.525106448699807,
            places=12)
        self.assertIn(
            "0.10930746469603118",
            aggregate_l2["normalized_equivalent_when_T_N_positive"])

    def test_coefficient_package_values_are_pinned(self):
        receipt = self.load_receipt()
        package = receipt["coefficient_package"]

        self.assertEqual(package["active_complex_character_count"], 122)
        self.assertEqual(package["active_real_channel_count"], 64)
        self.assertAlmostEqual(
            package["total_character_l1"],
            49.153988812629684,
            places=12)
        self.assertAlmostEqual(
            package["aggregate_character_l2"],
            5.525106448699807,
            places=12)
        self.assertEqual(
            package["per_modulus_active_character_count"]["286"],
            59)

    def test_finite_l2_diagnostics_remain_non_acceptance(self):
        receipt = self.load_receipt()
        finite = receipt["finite_diagnostic_boundary"]

        self.assertEqual(finite["observed_l2_row_count"], 348)
        self.assertEqual(finite["observed_row_local_l2_cap_violations"], 120)
        self.assertEqual(finite["observed_global_min_l2_cap_violations"], 301)
        self.assertIn("not acceptance conditions", finite["role"])

    def test_collapse_or_sleep_boundary_is_explicit(self):
        receipt = self.load_receipt()
        collapse = receipt["collapse_or_sleep_test"]

        self.assertIn("T_N>=P(N)>0", collapse["collapse_condition"])
        self.assertIn("ordinary strict-central binary Goldbach",
                      collapse["collapse_condition"])
        self.assertIn("Sleep q286", collapse["sleep_decision_if_collapsed"])
        self.assertIn("raw twisted binary-prime moments",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
