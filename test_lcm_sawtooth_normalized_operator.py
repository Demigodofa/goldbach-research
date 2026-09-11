import unittest

from lcm_sawtooth_cross_covariance import cyclic_sawtooth_covariance
from lcm_sawtooth_normalized_operator import (
    lcm_sawtooth_normalized_operator_probe,
)


class LcmSawtoothNormalizedOperatorTests(unittest.TestCase):
    def test_zero_variance_rows_have_zero_true_covariance(self):
        modulus, zero_period = 101, 10
        self.assertEqual(cyclic_sawtooth_covariance(
            modulus, zero_period, zero_period)["covariance"], 0)
        for other in range(2, 30):
            self.assertEqual(cyclic_sawtooth_covariance(
                modulus, zero_period, other)["covariance"], 0)

    def test_exact_operator_dominates_actual_rayleigh_ratio(self):
        receipt = lcm_sawtooth_normalized_operator_probe(101, 70, 4, 20)
        eigenvalue = receipt["absolute_normalized_operator_eigenvalue"]
        self.assertLessEqual(
            receipt["actual_mobius_absolute_rayleigh_ratio"],
            eigenvalue + 1e-10)
        self.assertLessEqual(
            abs(receipt["actual_mobius_signed_rayleigh_ratio"]),
            receipt["actual_mobius_absolute_rayleigh_ratio"] + 1e-10)
        self.assertGreaterEqual(
            receipt["actual_mobius_extremizer_squared_overlap"], 0)
        self.assertLessEqual(
            receipt["actual_mobius_extremizer_squared_overlap"], 1 + 1e-12)
        self.assertTrue(receipt["exact_normalized_operator_computed"])
        self.assertFalse(receipt["normalized_operator_subpower_bound_proved"])

    def test_known_zero_variance_support_falsifies_coarse_uniform_bound(self):
        receipt = lcm_sawtooth_normalized_operator_probe(101, 70, 4, 20)
        self.assertGreater(receipt["zero_variance_lcm_count"], 0)
        self.assertTrue(
            receipt["coarse_gcd_uniform_operator_bound_falsified"])

    def test_invalid_inputs(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            lcm_sawtooth_normalized_operator_probe(105, 10, 3, 24)


if __name__ == "__main__":
    unittest.main()
