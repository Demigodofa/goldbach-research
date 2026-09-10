import math
import unittest

import numpy as np

from signed_crt_discrepancy_probe import (
    _single_modulus_matrices,
    crt_interval_count_error,
    prime_averaged_signed_crt_discrepancy,
    prime_row_averaged_signed_crt_discrepancy,
    row_averaged_signed_crt_discrepancy,
    signed_crt_discrepancy_probe,
)


class SignedCrtDiscrepancyProbeTests(unittest.TestCase):
    def test_fractional_endpoint_formula_matches_exhaustive_counts(self):
        for modulus in range(1, 14):
            for lower in range(-5, 7):
                for upper in range(lower, 9):
                    for residue in range(modulus):
                        count, formula, direct_error = crt_interval_count_error(
                            lower, upper, residue, modulus)
                        direct_count = sum(
                            value % modulus == residue
                            for value in range(lower, upper + 1))
                        self.assertEqual(count, direct_count)
                        self.assertAlmostEqual(formula, direct_error, places=12)

    def test_matrix_is_hermitian_and_unsigned_certificate_dominates(self):
        divisors = (6, 7, 10, 11, 13, 14)
        discrepancy, _, unsigned, _ = _single_modulus_matrices(
            101, 3, 7, divisors)
        self.assertLess(np.max(np.abs(
            discrepancy - np.conjugate(discrepancy.T))), 1e-10)
        self.assertTrue(np.all(np.abs(discrepancy) <= unsigned + 1e-9))

    def test_matrix_matches_direct_signed_pair_count(self):
        modulus, shift_length, ell = 31, 2, 5
        divisors = (3, 5, 6, 7)
        discrepancy, _, _, rho = _single_modulus_matrices(
            modulus, shift_length, ell, divisors)
        modes = tuple(
            h for h in range(1, modulus)
            if modulus / (2 * math.pi * shift_length)
            < min(h, modulus - h)
            < modulus / (math.pi * shift_length))
        kernels = {
            separation: sum(np.exp(
                -2j * math.pi * h * separation / modulus) for h in modes)
            for separation in range(-modulus + 2, modulus - 1)
        }
        direct = np.zeros_like(discrepancy)
        for i, left in enumerate(divisors):
            left_positions = tuple(
                x for x in range(1, modulus)
                if (modulus * ell + x) % left == 0)
            for j, right in enumerate(divisors):
                right_positions = tuple(
                    y for y in range(1, modulus)
                    if (modulus * ell + y) % right == 0)
                exact = sum(kernels[x - y]
                            for x in left_positions for y in right_positions)
                gcd_value = math.gcd(left, right)
                common = math.lcm(left, right)
                density = sum(
                    kernels[s] * (modulus - 1 - abs(s)) / common
                    for s in kernels if s % gcd_value == 0)
                direct[i, j] = (1 - rho) * (exact - density)
        self.assertLess(np.max(np.abs(discrepancy - direct)), 1e-9)

    def test_resonant_operator_and_mobius_are_below_unsigned_bound(self):
        receipt = signed_crt_discrepancy_probe(1009, 5, 9, 50)
        self.assertGreater(receipt["signed_discrepancy_operator_norm"], 0)
        self.assertLessEqual(
            receipt["signed_discrepancy_operator_norm"],
            receipt["exact_entrywise_absolute_schur"] + 1e-10)
        self.assertLessEqual(
            receipt["exact_entrywise_absolute_schur"],
            receipt["proved_unsigned_endpoint_schur"] + 1e-10)
        self.assertLessEqual(
            receipt["mobius_signed_discrepancy_quotient"],
            receipt["signed_discrepancy_operator_norm"] + 1e-10)
        self.assertFalse(receipt["signed_discrepancy_bound_proved"])

    def test_repeated_prime_average_matches_single_prime(self):
        single = signed_crt_discrepancy_probe(1009, 5, 9, 50)
        averaged = prime_averaged_signed_crt_discrepancy(
            (1009,), 5, 9, 50)
        self.assertAlmostEqual(
            single["signed_discrepancy_operator_norm"],
            averaged["signed_discrepancy_operator_norm"], places=10)
        self.assertFalse(averaged["prime_average_cancellation_proved"])

    def test_one_row_average_matches_single_row(self):
        single = signed_crt_discrepancy_probe(1009, 5, 9, 50)
        averaged = row_averaged_signed_crt_discrepancy(
            1009, 5, 9, 1, 50)
        self.assertAlmostEqual(
            single["signed_discrepancy_operator_norm"],
            averaged["signed_discrepancy_operator_norm"], places=10)
        self.assertFalse(averaged["row_average_cancellation_proved"])

    def test_one_prime_one_row_joint_average_matches_single(self):
        single = signed_crt_discrepancy_probe(1009, 5, 9, 50)
        joint = prime_row_averaged_signed_crt_discrepancy(
            (1009,), 5, 9, 1, 50)
        self.assertAlmostEqual(
            single["signed_discrepancy_operator_norm"],
            joint["signed_discrepancy_operator_norm"], places=10)
        self.assertFalse(joint["joint_prime_row_cancellation_proved"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            signed_crt_discrepancy_probe(1001, 5, 9, 50)
        with self.assertRaises(ValueError):
            crt_interval_count_error(4, 3, 0, 2)
        with self.assertRaises(ValueError):
            prime_averaged_signed_crt_discrepancy((), 5, 9, 50)


if __name__ == "__main__":
    unittest.main()
