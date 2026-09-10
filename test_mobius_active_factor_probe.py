import unittest

import numpy as np

from mobius_active_factor_probe import (
    _dyadic_mobius_tails,
    finite_active_factor_probe,
)
from mobius_covariance_endpoint_probe import _actual_tail
from mobius_lag_spectral_probe import finite_mobius_lag_spectrum


class MobiusActiveFactorProbeTests(unittest.TestCase):
    def test_factor_bands_reconstruct_exact_tail(self):
        bands, tails = _dyadic_mobius_tails(2048, 4)
        self.assertEqual(bands[0], (4, 8))
        self.assertEqual(bands[-1][1], 2048)
        np.testing.assert_allclose(np.sum(tails, axis=0),
                                   _actual_tail(2048, 4, 0, 2048),
                                   atol=1e-12, rtol=0)

    def test_factor_matrix_reconstructs_active_dyadic_term(self):
        factor = finite_active_factor_probe(32000)
        spectral = finite_mobius_lag_spectrum(32000, padding_factor=2)
        self.assertEqual(len(factor["blocks"]), len(spectral["blocks"]))
        for left, right in zip(factor["blocks"], spectral["blocks"]):
            self.assertAlmostEqual(left["active_band_ratio"],
                                   right["active_band_signed_ratio"], places=10)
        self.assertFalse(factor["factor_diagonal_bound_proved"])


if __name__ == "__main__":
    unittest.main()
