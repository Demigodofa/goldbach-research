import json
import unittest
from pathlib import Path


class Q286WbssSignedWeightCircleTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-signed-weight-circle-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_bespoke_signed_weight_circle_method_or_collapse")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["major_minor_arc_estimate_proved"])
        self.assertFalse(
            receipt["signed_negative_region_distribution_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_exact_target_is_raw_signed_weighted_convolution(self):
        receipt = self.load_receipt()
        definitions = receipt["signed_weight_definitions"]
        target = receipt["exact_target"]

        self.assertIn("W_phi(N)=sum", definitions["raw_weighted_witness"])
        self.assertIn("W_+(N)-W_-(N)",
                      definitions["positive_negative_split"])
        self.assertIn("int_0^1", definitions["circle_integral"])
        self.assertIn("W_phi(N)>0", target["raw_pointwise_statement"])
        self.assertIn("sum_{u:phi(u)>0}",
                      target["equivalent_signed_region_statement"])

    def test_zero_mass_check_blocks_normalized_circularity(self):
        receipt = self.load_receipt()
        zero = receipt["zero_mass_non_circularity_check"]

        self.assertIn("W_phi(N)=W_+(N)=W_-(N)=0",
                      zero["if_T_N_zero"])
        self.assertIn("0>0", zero["strict_target_at_zero_mass"])
        self.assertIn("normalized theorem", zero["meaning"])

    def test_collapse_classifier_is_explicit(self):
        receipt = self.load_receipt()
        classifier = receipt["collapse_classifier"]

        self.assertIn("directly for every sufficiently large covered N",
                      classifier["survives_if"])
        self.assertIn("T_N>0", classifier["collapses_if"])
        self.assertIn("normalizing by T_N before raw support exists",
                      classifier["invalid_substitutes"])
        self.assertIn("sleep q286", classifier["sleep_condition"])

    def test_preserves_signed_region_constants(self):
        receipt = self.load_receipt()
        constants = receipt["major_minor_arc_target"][
            "finite_constants_to_preserve"]

        self.assertAlmostEqual(
            constants["shape_threshold_minimum"],
            0.48729403831397616,
            places=12)
        self.assertAlmostEqual(
            constants["minimum_local_uniform_shape_margin"],
            0.10534041937277128,
            places=12)
        self.assertEqual(
            constants["active_character_l2_related_but_unproved"],
            "q286_active_character_L2_payment")

    def test_decision_names_next_major_arc_test(self):
        receipt = self.load_receipt()

        self.assertIn("raw pointwise signed weighted binary-prime convolution",
                      receipt["decision"])
        self.assertIn("symbolic major-arc local-factor decomposition",
                      receipt["decision"])
        self.assertIn("T_N>0", receipt["decision"])
        self.assertIn("not a theorem", receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
