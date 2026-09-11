import unittest

from lcm_sawtooth_source_tensor import (
    leading_lag_source_tensor_receipt,
    source_tensor_receipt,
)


class SourceTensorTests(unittest.TestCase):
    def test_lag_182_tensor_decomposition(self):
        receipt = source_tensor_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["gcd_lag_period"], 182)
        self.assertEqual(receipt["quotient_period"], 55)
        self.assertEqual(receipt["quotient_primes"], (5, 11))
        self.assertEqual(
            receipt["sector_eigenvalues"],
            {(): 27, (11,): -3, (5,): -9, (5, 11): 1})
        self.assertLess(
            receipt["maximum_sample_natural_scale_relative_error"], 1e-12)
        self.assertLess(
            receipt["phase_removed_target_relative_error"], 1e-12)
        self.assertTrue(receipt["tensor_difference_graph_identity_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            source_tensor_receipt(lag=0)
        with self.assertRaises(ValueError):
            source_tensor_receipt(families=((77, 65),))
        with self.assertRaises(ValueError):
            source_tensor_receipt(tolerance=-1)

    def test_tensor_decomposition_across_leading_lags(self):
        receipt = leading_lag_source_tensor_receipt()
        self.assertEqual(receipt["lags"], (140, 154, 156, 182, 240))
        self.assertEqual(
            receipt["quotient_primes"],
            {140: (11, 13), 154: (5, 13), 156: (5, 7, 11),
             182: (5, 11), 240: (7, 11, 13)})
        self.assertLess(
            receipt["maximum_sample_natural_scale_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_phase_removed_target_relative_error"], 1e-12)
        self.assertTrue(
            receipt["all_tensor_difference_graph_identities_pass"])
        sectors = receipt["sector_phase_removed_mean_correlations"]
        self.assertAlmostEqual(sectors[140][()][0], -85437 / 4, places=7)
        self.assertAlmostEqual(sectors[240][()][0], -27225 / 2, places=7)
        self.assertAlmostEqual(sectors[156][(5,)][0], 12375 / 2, places=7)
        self.assertAlmostEqual(sectors[182][(5,)][0], 12375 / 4, places=7)
        self.assertAlmostEqual(sectors[182][(11,)][0], 11011 / 30, places=7)
        self.assertGreater(abs(sectors[154][(5, 13)][0]), 1000)
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
