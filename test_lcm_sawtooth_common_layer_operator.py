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
        self.assertGreaterEqual(receipt["actual_extremizer_squared_overlap"], 0)
        self.assertLessEqual(receipt["actual_extremizer_squared_overlap"], 1)
        self.assertTrue(
            receipt["common_layer_generalized_operator_computed"])
        self.assertFalse(receipt["common_layer_subpower_bound_proved"])

    def test_project_sampler_is_finite_only(self):
        receipt = project_common_layer_operator_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)
        self.assertTrue(
            receipt["finite_project_common_layer_operator_measurement"])
        self.assertFalse(receipt["common_layer_subpower_bound_proved"])


if __name__ == "__main__":
    unittest.main()
