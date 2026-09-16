import json
import unittest
from pathlib import Path


class Q286WbssK286CoefficientNormBurdenTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-coefficient-norm-burden.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_k286_coefficient_norm_burden_unproved")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["k286_pointwise_lower_bound_proved"])
        self.assertFalse(
            receipt["twisted_prime_pair_moment_theorem_proved"])
        self.assertFalse(receipt["major_minor_arc_estimate_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_active_support_is_smaller_than_nominal_character_space(self):
        receipt = self.load_receipt()
        package = receipt["coefficient_package"]

        self.assertEqual(package["available_character_count"], 99)
        self.assertEqual(package["active_nonzero_character_count"], 50)
        self.assertEqual(package["zero_available_character_count"], 49)
        self.assertLess(
            package["max_abs_zero_available_coefficient"], 1e-8)
        self.assertLess(
            package["max_abs_outside_11x13_coefficient"], 1e-8)
        self.assertLess(package["descent_relative_error"], 1e-12)
        self.assertLess(package["reconstruction_relative_error"], 1e-12)

    def test_principal_normalized_norms_and_caps_are_pinned(self):
        receipt = self.load_receipt()
        norms = receipt["coefficient_package"][
            "principal_normalized_norms"]
        burdens = receipt["sufficient_burdens"]

        self.assertAlmostEqual(norms["l1"], 32.42815568567079, places=12)
        self.assertAlmostEqual(norms["l2"], 4.628530101718351, places=12)
        self.assertAlmostEqual(norms["linf"], 0.8166661291234342,
                               places=12)
        self.assertAlmostEqual(
            burdens["uniform_linf_moment_cap"]["required_cap"],
            0.00542441385158965,
            places=15)
        self.assertAlmostEqual(
            burdens["aggregate_l2_moment_cap"]["required_cap"],
            0.038004233097145394,
            places=15)

    def test_singular_structure_names_two_mode_candidate(self):
        receipt = self.load_receipt()
        singular = receipt["coefficient_package"]["singular_structure"]
        two_mode = receipt["sufficient_burdens"][
            "dominant_two_singular_mode_target"]

        self.assertEqual(singular["matrix_shape"], [9, 11])
        self.assertEqual(singular["numerical_rank"], 9)
        self.assertAlmostEqual(
            singular["effective_singular_rank"],
            1.986349842039335,
            places=12)
        self.assertAlmostEqual(
            singular["top_two_singular_energy_fraction"],
            0.9760410444893588,
            places=12)
        self.assertIn("first two singular directions",
                      two_mode["statement"])
        self.assertAlmostEqual(
            two_mode["residual_singular_energy_fraction"],
            0.02395895551064118,
            places=12)

    def test_notation_preserves_raw_pointwise_theorem_boundary(self):
        receipt = self.load_receipt()
        notation = receipt["normalized_moment_notation"]

        self.assertIn("D_chi^P(N)/P0_a(N)", notation["moment"])
        self.assertIn("Re sum_chi kappa_chi*delta_chi(N)",
                      notation["target"])
        self.assertIn("not a theorem", receipt["status_boundary"])
        self.assertIn("proves no such pointwise moment theorem",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
