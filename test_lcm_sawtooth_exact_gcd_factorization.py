import math
import cmath
import unittest

from lcm_sawtooth_cross_covariance import cyclic_sawtooth_covariance
from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    lcm_sawtooth_exact_gcd_factorization_probe,
    project_exact_gcd_scale_probe,
    sawtooth_gcd_kernel_numerator,
    sawtooth_gcd_mobius_transform,
)


class LcmSawtoothExactGcdFactorizationTests(unittest.TestCase):
    def test_one_variable_covariance_identity_exhaustively(self):
        for modulus in (101, 103):
            for left in range(2, 25):
                for right in range(2, 25):
                    common = math.gcd(left, right)
                    expected = sawtooth_gcd_kernel_numerator(
                        modulus, common) / (left * right)
                    actual = cyclic_sawtooth_covariance(
                        modulus, left, right)["covariance"]
                    self.assertAlmostEqual(actual, expected, places=12)

    def test_mobius_transform_inverts_on_squarefree_divisors(self):
        for modulus in (101, 103):
            for value in (1, 2, 6, 30, 210):
                reconstructed = sum(
                    sawtooth_gcd_mobius_transform(modulus, divisor)
                    for divisor, _
                    in _squarefree_divisors_with_complement_mobius(value))
                self.assertEqual(
                    reconstructed,
                    sawtooth_gcd_kernel_numerator(modulus, value))

    def test_transform_is_primitive_fourier_energy(self):
        for modulus in (101, 103):
            for divisor in (2, 3, 5, 6, 10, 15, 30):
                residue = (modulus - 1) % divisor
                fourier_energy = sum(abs(sum(
                    cmath.exp(2j * math.pi * frequency * position / divisor)
                    for position in range(residue))) ** 2
                    for frequency in range(1, divisor)
                    if math.gcd(frequency, divisor) == 1)
                transform = sawtooth_gcd_mobius_transform(modulus, divisor)
                self.assertGreaterEqual(transform, 0)
                self.assertAlmostEqual(transform, fourier_energy, places=9)

    def test_sparse_forms_match_dense_forms(self):
        # Rebuild dense forms from the coefficient support exposed by a small
        # independent divisor-pair enumeration.
        modulus, ell, lower, upper = 101, 70, 4, 20
        receipt = lcm_sawtooth_exact_gcd_factorization_probe(
            modulus, ell, lower, upper)
        from lcm_sawtooth_incomplete_covariance import (
            _evaluate_polynomial, _lcm_coefficient_polynomials)
        from mobius_covariance_lag_probe import _mobius_values
        mobius = _mobius_values(upper)
        divisors = tuple(value for value in range(lower + 1, upper + 1)
                         if mobius[value])
        polynomials = _lcm_coefficient_polynomials(divisors, mobius)
        logarithm = math.log(modulus * ell)
        coefficients = {q: float(_evaluate_polynomial(poly, logarithm))
                        for q, poly in polynomials.items()}
        signed = absolute = 0.0
        for left, left_value in coefficients.items():
            for right, right_value in coefficients.items():
                covariance = cyclic_sawtooth_covariance(
                    modulus, left, right)["covariance"]
                signed += left_value * right_value * covariance
                absolute += abs(left_value * right_value) * covariance
        self.assertAlmostEqual(
            receipt["exact_signed_complete_energy"], signed, places=7)
        self.assertAlmostEqual(
            receipt["exact_termwise_absolute_complete_energy"],
            absolute, places=7)
        self.assertTrue(receipt["exact_sparse_gcd_factorization_proved"])
        self.assertTrue(
            receipt["primitive_frequency_weights_nonnegative_proved"])
        self.assertFalse(receipt["subpower_factorized_bound_proved"])

    def test_project_sampler(self):
        receipt = project_exact_gcd_scale_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)

    def test_invalid_squarefree_transform_input(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            _squarefree_divisors_with_complement_mobius(12)


if __name__ == "__main__":
    unittest.main()
