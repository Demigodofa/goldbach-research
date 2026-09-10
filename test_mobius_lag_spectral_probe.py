import unittest

import numpy as np

from mobius_dyadic_lag_gate import finite_dyadic_lag_gate
from mobius_lag_spectral_probe import (
    dyadic_spectral_decomposition,
    finite_mobius_lag_spectrum,
)


class MobiusLagSpectralProbeTests(unittest.TestCase):
    def test_exact_identity_for_arbitrary_complex_array(self):
        rng = np.random.default_rng(91827)
        values = (rng.normal(size=(7, 11))
                  + 1j * rng.normal(size=(7, 11)))
        prior = None
        for padding_factor in (2, 5, 11):
            result = dyadic_spectral_decomposition(
                values, [1, 4, 8], padding_factor)
            direct = []
            for block in result["blocks"]:
                self.assertAlmostEqual(
                    block["identity_error"], 0.0, places=11)
                self.assertAlmostEqual(
                    sum(block["quadrants"].values()),
                    block["spectral_covariance"], places=11)
                direct.append(block["direct_covariance"])
            if prior is not None:
                np.testing.assert_allclose(direct, prior, atol=1e-11, rtol=0)
            prior = direct

    def test_actual_spectrum_matches_direct_dyadic_gate(self):
        spectral = finite_mobius_lag_spectrum(32000)
        direct = finite_dyadic_lag_gate(32000)
        self.assertEqual(len(spectral["blocks"]), len(direct["blocks"]))
        for left, right in zip(spectral["blocks"], direct["blocks"]):
            self.assertEqual((left["lag_first"], left["lag_last"]),
                             (right["lag_first"], right["lag_last"]))
            self.assertAlmostEqual(left["signed_ratio"],
                                   right["signed_ratio"], places=11)
            self.assertAlmostEqual(
                left["positive_spectral_ratio"]
                - left["negative_spectral_ratio"],
                left["signed_ratio"], places=11)
            self.assertAlmostEqual(
                left["active_band_signed_ratio"]
                + left["outside_band_signed_ratio"],
                left["signed_ratio"], places=11)
        self.assertGreaterEqual(
            spectral["maximum_positive_active_band_ratio"], 0.0)
        self.assertFalse(spectral["joint_spectral_saving_proved"])


if __name__ == "__main__":
    unittest.main()
