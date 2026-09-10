import unittest

from mobius_aligned_lag_probe import finite_aligned_lag_probe
from mobius_dyadic_lag_gate import finite_dyadic_lag_gate


class MobiusDyadicLagGateTests(unittest.TestCase):
    def test_rejects_block_outside_required_annulus(self):
        with self.assertRaises(ValueError):
            finite_dyadic_lag_gate(32000, 2)

    def test_blocks_partition_exact_cross_row_covariance(self):
        dyadic = finite_dyadic_lag_gate(32000)
        lag = finite_aligned_lag_probe(32000)
        covariance = sum(block["covariance"] for block in dyadic["blocks"])
        self.assertAlmostEqual(covariance,
                               sum(lag["lag_contributions"][1:]), places=5)
        covered = [delta
                   for block in dyadic["blocks"]
                   for delta in range(block["lag_first"],
                                      block["lag_last"] + 1)]
        self.assertEqual(covered, list(range(1, dyadic["cofactor_left"])))
        self.assertGreater(dyadic["maximum_positive_ratio"], 0)
        self.assertTrue(all(
            block["absolute_modulus_ratio"] >= abs(block["signed_ratio"])
            for block in dyadic["blocks"]))
        self.assertFalse(dyadic["dyadic_h_inverse_sublemma_proved"])


if __name__ == "__main__":
    unittest.main()
