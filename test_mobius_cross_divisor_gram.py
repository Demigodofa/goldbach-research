import unittest

import numpy as np

from mobius_active_factor_probe import _dyadic_mobius_tails
from mobius_cross_divisor_gram import (
    _progression_vectors,
    finite_cross_divisor_gram,
)
from near_cutoff_geometric_bound import _active_modes


class MobiusCrossDivisorGramTests(unittest.TestCase):
    def test_progression_vectors_reconstruct_first_factor_band(self):
        N, H, m, ell, V = 32000, 2, 457, 9, 4
        bands, tails = _dyadic_mobius_tails(N, V)
        mobius = np.array([-1, 1, -1])  # mu(5),mu(6),mu(7)
        modes, vectors = _progression_vectors(m, H, ell, (5, 6, 7))
        row = np.zeros(m)
        row[1:] = tails[0, m * ell + 1:m * (ell + 1)]
        transform = np.fft.fft(row)
        centered = transform + row.sum() / (m - 1)
        np.testing.assert_allclose(mobius @ vectors, centered[modes],
                                   atol=1e-9, rtol=0)
        self.assertEqual(tuple(modes), _active_modes(m, H))
        self.assertEqual(bands[0], (4, 8))

    def test_gram_receipt_has_exact_energy_ordering(self):
        receipt = finite_cross_divisor_gram(32000)
        self.assertGreaterEqual(receipt["mobius_energy"], 0)
        self.assertGreaterEqual(receipt["uniform_largest_eigenvalue"],
                                receipt["mobius_rayleigh_ratio"])
        self.assertLessEqual(receipt["uniform_smallest_eigenvalue"],
                             receipt["mobius_rayleigh_ratio"])
        self.assertFalse(receipt["divisor_quasi_orthogonality_proved"])


if __name__ == "__main__":
    unittest.main()
