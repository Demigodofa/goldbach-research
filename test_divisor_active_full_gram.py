import unittest

import numpy as np

from divisor_active_full_gram import (
    _full_collision_gram,
    finite_active_full_comparison,
    single_modulus_active_full_comparison,
)


class DivisorActiveFullGramTests(unittest.TestCase):
    def test_collision_formula_matches_direct_full_frequency_gram(self):
        modulus, ell = 457, 9
        divisors = (5, 6, 7)
        rows = np.zeros((len(divisors), modulus))
        for index, divisor in enumerate(divisors):
            first = modulus * ell // divisor + 1
            last = (modulus * (ell + 1) - 1) // divisor
            cofactors = np.arange(first, last + 1, dtype=np.int64)
            residues = divisor * cofactors - modulus * ell
            rows[index, residues] = np.log(cofactors)
        transforms = np.fft.fft(rows, axis=1)
        centered = transforms + rows.sum(axis=1)[:, None] / (modulus - 1)
        direct = centered[:, 1:] @ np.conjugate(centered[:, 1:].T)
        np.testing.assert_allclose(
            _full_collision_gram(modulus, ell, divisors), direct,
            atol=2e-8, rtol=2e-12)

    def test_active_full_generalized_receipt_is_ordered(self):
        receipt = finite_active_full_comparison(32000)
        self.assertGreater(receipt["mobius_active_over_rho_full"], 0)
        self.assertGreaterEqual(
            receipt["uniform_largest_generalized_eigenvalue"],
            receipt["mobius_active_over_rho_full"])
        self.assertLessEqual(
            receipt["uniform_smallest_generalized_eigenvalue"],
            receipt["mobius_active_over_rho_full"])
        self.assertFalse(receipt["active_full_matrix_bound_proved"])

    def test_single_modulus_stress_receipt(self):
        receipt = single_modulus_active_full_comparison(1009, 5, 9, 3, 8)
        self.assertEqual(receipt["divisor_count"], 5)
        self.assertGreaterEqual(
            receipt["uniform_largest_generalized_eigenvalue"],
            receipt["mobius_active_over_rho_full"])


if __name__ == "__main__":
    unittest.main()
