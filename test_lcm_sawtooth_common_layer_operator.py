import unittest

from lcm_sawtooth_common_layer_operator import (
    common_layer_operator_probe,
    project_common_layer_operator_probe,
)
from lcm_sawtooth_common_prime_cancellation import (
    common_prime_cancellation_probe,
)


class LcmSawtoothCommonLayerOperatorTests(unittest.TestCase):
    def test_actual_layer_rayleigh_matches_dominant_block_quotient(self):
        receipt = common_layer_operator_probe(101, 70, 4, 20)
        split = common_prime_cancellation_probe(101, 70, 4, 20)
        self.assertEqual(
            receipt["dominant_block_range"], split["dominant_block_range"])
        self.assertAlmostEqual(
            receipt["actual_mobius_common_layer_quotient"],
            split["dominant_block"]["actual_residual_quotient"])
        self.assertGreaterEqual(
            receipt["largest_common_layer_generalized_eigenvalue"],
            receipt["actual_mobius_common_layer_quotient"])
        self.assertGreater(
            receipt["largest_absolute_layer_generalized_eigenvalue"], 0)
        self.assertGreater(
            receipt["layer_schur_over_coercivity_bound"],
            receipt["largest_common_layer_generalized_eigenvalue"])
        self.assertEqual(
            len(receipt["individual_layers"]),
            receipt["active_common_part_count"])
        self.assertTrue(receipt["singleton_common_tail_verified"])
        self.assertTrue(receipt["large_common_part_singleton_tail_proved"])
        self.assertGreaterEqual(receipt["actual_extremizer_squared_overlap"], 0)
        self.assertLessEqual(receipt["actual_extremizer_squared_overlap"], 1)
        self.assertTrue(
            receipt["common_layer_generalized_operator_computed"])
        self.assertAlmostEqual(
            receipt["separated_over_actual_common_layer_diagonal"],
            receipt["separated_common_layer_diagonal"]
            / receipt["actual_combined_common_layer_diagonal"])
        self.assertAlmostEqual(
            receipt["separated_over_actual_common_layer_base_diagonal"],
            receipt["separated_common_layer_base_diagonal"]
            / receipt["actual_combined_common_layer_base_diagonal"])
        self.assertGreater(receipt["actual_base_diagonal_fraction"], 0)
        self.assertGreaterEqual(
            receipt["maximum_pointwise_base_separated_over_actual"], 1)
        self.assertIsNotNone(receipt["maximum_pointwise_base_witness"])
        self.assertEqual(
            receipt["maximum_pointwise_base_witness"]["modulus"], 101)
        self.assertGreaterEqual(
            receipt[
                "maximum_high_conductor_pointwise_base_separated_over_4omega_actual"],
            0)
        self.assertGreaterEqual(
            receipt[
                "maximum_all_high_conductor_pointwise_base_separated_over_4omega_actual"],
            0)
        self.assertFalse(receipt["pointwise_base_4omega_bound_proved"])
        self.assertFalse(receipt["common_layer_subpower_bound_proved"])
        self.assertFalse(
            receipt["common_layer_diagonal_interference_bound_proved"])

    def test_project_sampler_is_finite_only(self):
        receipt = project_common_layer_operator_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)
        self.assertTrue(
            receipt["finite_project_common_layer_operator_measurement"])
        self.assertGreater(
            receipt[
                "maximum_pointwise_base_4omega_normalized_min_median_max"][2],
            0)
        self.assertIsNotNone(receipt["maximum_pointwise_base_witness"])
        self.assertGreaterEqual(
            receipt[
                "maximum_high_conductor_pointwise_base_4omega_normalized_min_median_max"][2],
            0)
        self.assertGreaterEqual(
            receipt[
                "maximum_all_high_conductor_pointwise_base_4omega_normalized_min_median_max"][2],
            0)
        self.assertFalse(receipt["pointwise_base_4omega_bound_proved"])
        self.assertFalse(receipt["common_layer_subpower_bound_proved"])

    def test_all_high_scan_retains_project_scaled_counterexample(self):
        receipt = common_layer_operator_probe(16001, 1252, 11, 190)
        witness = receipt[
            "maximum_all_high_conductor_pointwise_base_witness"]
        self.assertTrue(
            receipt[
                "all_high_conductor_pointwise_base_4omega_falsified_in_measurement"])
        self.assertEqual(witness["divisor"], 2310)
        self.assertGreater(witness["divisor"], 11 * 190)
        self.assertAlmostEqual(
            witness["separated_over_4omega_actual"], 4.5356909415)


if __name__ == "__main__":
    unittest.main()
