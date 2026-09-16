import json
import unittest
from pathlib import Path


class Q286WbssRawCharacterCircleDecompositionTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-raw-character-circle-decomposition.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_decomposition_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_raw_character_circle_method_decomposition_"
            "bridge_unproved")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["circle_method_estimate_proved"])
        self.assertFalse(receipt["raw_character_moment_theorem_proved"])
        self.assertFalse(receipt["adverse_drag_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])
        self.assertFalse(receipt["finite_evidence_acceptance_condition"])

    def test_exact_integral_identity_contains_raw_subtraction(self):
        receipt = self.load_receipt()
        identities = receipt["exact_fourier_identities"]

        self.assertIn("P(n)=log(n) if n is prime",
                      receipt["notation"]["prime_log_weight"])
        self.assertIn("int_0^1", identities["central_mass"])
        self.assertIn("= T_N", identities["central_mass"])
        self.assertIn("C_{d,chi}(N)", identities["twisted_pair_mass"])
        self.assertIn("U_{a,d,chi}*C_0(N)",
                      identities["raw_character_moment"])
        self.assertIn("chi_d(n)-U_{a,d,chi}",
                      identities["single_weight_form"])

    def test_zero_mass_check_confirms_strict_raw_non_circular_shape(self):
        receipt = self.load_receipt()
        zero = receipt["zero_mass_check"]

        self.assertIn("C_0(N)=0", zero["if_T_N_is_zero"])
        self.assertIn("D_raw_{d,chi}(N)=0", zero["if_T_N_is_zero"])
        self.assertIn("0<0", zero["strict_L2_target_at_zero_mass"])
        self.assertIn("non-circular theorem shapes", zero["conclusion"])
        self.assertIn("not confirmed", zero["conclusion"])

    def test_collapse_classifier_requires_direct_pointwise_estimate(self):
        receipt = self.load_receipt()
        classifier = receipt["collapse_classifier"]
        targets = receipt["universal_pointwise_targets"]

        self.assertIn("without first assuming pointwise T_N>0",
                      classifier["survives_as_q286_proof_engine_if"])
        self.assertIn("first establishes or assumes T_N>0",
                      classifier["collapses_if"])
        self.assertIn("L2 is a target, not an accepted bridge",
                      classifier["logical_bridge_status"])
        self.assertIn("adverse_drag_raw(N)<local_main_raw(N)",
                      targets["acceptance_condition"])
        self.assertIn("Finite evidence is not an acceptance condition",
                      targets["acceptance_condition"])

    def test_inherited_numbers_are_pinned(self):
        receipt = self.load_receipt()
        numbers = receipt["inherited_numbers"]

        self.assertEqual(numbers["active_complex_character_count"], 122)
        self.assertEqual(numbers["active_real_channel_count"], 64)
        self.assertAlmostEqual(
            numbers["aggregate_character_l2"],
            5.525106448699807,
            places=12)
        self.assertAlmostEqual(
            numbers["aggregate_character_moment_l2_cap_normalized"],
            0.10930746469603118,
            places=12)
        self.assertEqual(numbers["observed_l2_row_count"], 348)
        self.assertEqual(numbers["observed_row_local_l2_cap_violations"], 120)
        self.assertEqual(
            numbers["observed_global_min_l2_cap_violations"], 301)

    def test_visualization_is_exploratory_not_evidence(self):
        receipt = self.load_receipt()
        visual = receipt["visualization_candidate"]

        self.assertIn("Exploratory only", visual["role"])
        self.assertEqual(visual["x_axis"], "log(N).")
        self.assertIn("not a residue label", visual["y_axis"])
        self.assertIn("Exact N", visual["linked_table_payload"])


if __name__ == "__main__":
    unittest.main()
