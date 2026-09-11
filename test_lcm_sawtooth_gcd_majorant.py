import math
import unittest

from lcm_sawtooth_gcd_majorant import (
    _squarefree_divisor_jordan_pairs,
    lcm_sawtooth_gcd_majorant_probe,
    project_gcd_majorant_scale_probe,
)
from lcm_sawtooth_incomplete_covariance import (
    _evaluate_polynomial,
    _lcm_coefficient_polynomials,
)
from mobius_covariance_lag_probe import _mobius_values


class LcmSawtoothGcdMajorantTests(unittest.TestCase):
    def test_jordan_divisor_identity(self):
        for value in (1, 2, 6, 30, 210):
            pairs = _squarefree_divisor_jordan_pairs(value)
            self.assertEqual(sum(jordan for _, jordan in pairs), value ** 2)
            self.assertEqual(tuple(sorted(divisor for divisor, _ in pairs)),
                             tuple(divisor for divisor in range(1, value + 1)
                                   if value % divisor == 0))

    def test_sparse_factorization_matches_dense_gcd_sum(self):
        modulus, ell, lower, upper = 101, 70, 4, 20
        receipt = lcm_sawtooth_gcd_majorant_probe(
            modulus, ell, lower, upper)
        mobius = _mobius_values(upper)
        divisors = tuple(value for value in range(lower + 1, upper + 1)
                         if mobius[value])
        polynomials = _lcm_coefficient_polynomials(divisors, mobius)
        logarithm = math.log(modulus * ell)
        coefficients = {
            q: float(_evaluate_polynomial(polynomial, logarithm))
            for q, polynomial in polynomials.items()}
        dense = .25 * sum(
            abs(left_value * right_value)
            * math.gcd(left, right) ** 2 / (left * right)
            for left, left_value in coefficients.items()
            for right, right_value in coefficients.items())
        self.assertAlmostEqual(receipt["sparse_gcd_majorant"], dense, places=8)
        self.assertGreaterEqual(
            receipt["gcd_majorant_over_diagonal"], 1.0 - 1e-12)
        self.assertTrue(receipt["sparse_gcd_factorization_proved"])
        self.assertFalse(receipt["gcd_majorant_subpower_bound_proved"])

    def test_project_sampler(self):
        receipt = project_gcd_majorant_scale_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)
        self.assertLessEqual(
            receipt["ratio_minimum"], receipt["ratio_median"])
        self.assertLessEqual(
            receipt["ratio_median"], receipt["ratio_maximum"])

    def test_invalid_inputs(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            _squarefree_divisor_jordan_pairs(12)
        with self.assertRaisesRegex(ValueError, "prime"):
            lcm_sawtooth_gcd_majorant_probe(105, 10, 3, 24)


if __name__ == "__main__":
    unittest.main()
