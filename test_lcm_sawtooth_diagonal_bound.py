import math
import unittest

from lcm_sawtooth_diagonal_bound import (
    cyclic_sawtooth_variance,
    lcm_sawtooth_diagonal_probe,
)


class LcmSawtoothDiagonalTests(unittest.TestCase):
    def test_sawtooth_variance_matches_complete_period(self):
        modulus, period = 101, 14
        values = []
        for ell in range(period):
            X = modulus * ell
            count = ((X + modulus - 1) // period - X // period)
            values.append(count - (modulus - 1) / period)
        direct = sum(value ** 2 for value in values) / period
        self.assertAlmostEqual(
            direct, cyclic_sawtooth_variance(modulus, period), places=12)

    def test_diagonal_cauchy_and_gcd_bounds(self):
        receipt = lcm_sawtooth_diagonal_probe(101, 5, 3, 14)
        self.assertLessEqual(
            receipt["diagonal_fourier_energy"],
            receipt["exact_cauchy_upper_bound"] + 1e-10)
        self.assertLessEqual(
            receipt["exact_cauchy_upper_bound"],
            receipt["reciprocal_multiplicity_upper_bound"] + 1e-10)
        self.assertAlmostEqual(
            receipt["reciprocal_lcm_pair_mass"],
            receipt["gcd_decomposition_pair_mass"], places=10)
        self.assertLessEqual(
            receipt["maximum_lcm_pair_multiplicity"],
            receipt["maximum_three_to_omega"])
        self.assertTrue(receipt["diagonal_bound_proved"])
        self.assertFalse(receipt["cross_lcm_covariance_bound_proved"])

    def test_invalid_ranges_are_rejected(self):
        with self.assertRaises(ValueError):
            cyclic_sawtooth_variance(101, 1)
        with self.assertRaisesRegex(ValueError, "coprime"):
            cyclic_sawtooth_variance(10, 14)
        with self.assertRaisesRegex(ValueError, "prime"):
            lcm_sawtooth_diagonal_probe(105, 5, 3, 14)
        with self.assertRaisesRegex(ValueError, "squarefree"):
            lcm_sawtooth_diagonal_probe(101, 5, 3, 4)


if __name__ == "__main__":
    unittest.main()
