import unittest

from mobius_factor_eigen_probe import factor_eigen_receipt


class MobiusFactorEigenProbeTests(unittest.TestCase):
    def test_generalized_spectrum_reconstructs_actual_factor_vector(self):
        result = factor_eigen_receipt(32000)
        self.assertEqual(len(result["principal_eigenvalue_shares"]), 3)
        self.assertEqual(len(result["generalized_off_over_principal_eigenvalues"]), 3)
        self.assertEqual(len(result["all_factor_generalized_spectral_weights"]), 3)
        self.assertAlmostEqual(sum(result["principal_eigenvalue_shares"]), 1.0,
                               places=12)
        self.assertAlmostEqual(result["spectral_weight_sum"], 1.0, places=12)
        self.assertAlmostEqual(
            result["reconstructed_all_factor_off_over_principal"],
            result["direct_all_factor_off_over_principal"], places=12)
        self.assertGreater(result["principal_condition_number"], 1)
        self.assertGreater(result["smallest_principal_cosine_with_all_factor"],
                           0.98)
        self.assertFalse(result["identity_alone_proves_active_band_bound"])


if __name__ == "__main__":
    unittest.main()
