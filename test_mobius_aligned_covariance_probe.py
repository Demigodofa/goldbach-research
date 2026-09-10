import unittest

from mobius_aligned_covariance_probe import finite_aligned_covariance_split


class MobiusAlignedCovarianceProbeTests(unittest.TestCase):
    def test_components_recombine_and_expose_opposite_large_signs(self):
        result = finite_aligned_covariance_split(32000)
        normalized = result["normalized"]
        self.assertAlmostEqual(result["recombination_error"], 0.0, places=6)
        self.assertAlmostEqual(
            normalized["total_off"],
            normalized["point"] + normalized["same_row_nonpoint"]
            + normalized["cross_row"], places=12)
        self.assertLess(normalized["same_row_nonpoint"], -1)
        self.assertGreater(normalized["cross_row"], 1)
        self.assertLess(abs(normalized["point"]), 1e-4)
        self.assertFalse(result["signed_off_diagonal_estimate_proved"])


if __name__ == "__main__":
    unittest.main()
