import unittest

from mobius_factor_covariance_probe import finite_factor_covariance_probe


class MobiusFactorCovarianceProbeTests(unittest.TestCase):
    def test_component_matrices_recombine_and_are_hermitian(self):
        result = finite_factor_covariance_probe(32000)
        diagonal = result["principal_matrix"]
        off = result["off_matrix"]
        self.assertEqual(result["labels"], ("lower", "balanced", "upper"))
        self.assertGreater(result["prime_count"], 0)
        for row in range(3):
            for column in range(3):
                self.assertAlmostEqual(diagonal[row][column],
                                       diagonal[column][row], places=7)
                self.assertAlmostEqual(off[row][column],
                                       off[column][row], places=7)
        self.assertAlmostEqual(sum(map(sum, diagonal)),
                               result["total_diagonal"], places=6)
        self.assertAlmostEqual(sum(map(sum, off)), result["total_off"], places=6)
        self.assertAlmostEqual(
            result["diagonal_component_off"] + result["cross_component_off"],
            result["total_off"], places=6)
        self.assertLess(result["maximum_imaginary_roundoff"], 1e-5)


if __name__ == "__main__":
    unittest.main()
