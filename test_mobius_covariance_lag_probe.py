import unittest

from mobius_covariance_lag_probe import finite_actual_tail_lag_probe


class MobiusCovarianceLagProbeTests(unittest.TestCase):
    def test_finite_components_recombine(self):
        result = finite_actual_tail_lag_probe(20000)
        self.assertAlmostEqual(
            result["off"],
            result["literal_residue_diagonal"] + result["off_diagonal"],
            places=6,
        )
        self.assertAlmostEqual(
            result["off_diagonal"],
            result["leading_W_off_diagonal"]
            + result["centering_off_diagonal"],
            places=6,
        )
        self.assertAlmostEqual(
            result["band"],
            result["off"] + result["principal_diagonal"],
            places=6,
        )


if __name__ == "__main__":
    unittest.main()
