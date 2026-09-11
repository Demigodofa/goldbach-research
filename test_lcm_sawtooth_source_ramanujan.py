import math
import unittest

import numpy as np

from lcm_sawtooth_source_ramanujan import (
    _conditioned_unit_exponential_sum,
    _endpoint_modes,
    source_ramanujan_mean_receipt,
)


class SourceRamanujanTests(unittest.TestCase):
    def test_endpoint_modes_match_direct_endpoint_value(self):
        period = 10010
        denominator = 77
        numerator = 12
        for residue in (1, 23, 9973):
            expanded = sum(
                coefficient * np.exp(
                    2j * np.pi * frequency * residue / period)
                for frequency, coefficient in _endpoint_modes(
                    period, denominator, numerator))
            root = np.exp(2j * np.pi * numerator / denominator)
            direct = (root ** residue - root) / (root - 1)
            self.assertLess(abs(expanded - direct), 1e-11)

    def test_conditioned_sum_matches_direct_unit_enumeration(self):
        period = 10010
        lag = 182
        for difference in (182, 3 * 182, 54 * 182):
            for frequency in (0, 1, 77, 143, 10009):
                direct = sum(
                    np.exp(2j * np.pi * frequency * residue / period)
                    for residue in range(period)
                    if math.gcd(residue, period) == 1
                    and residue * difference % period == lag)
                factored = _conditioned_unit_exponential_sum(
                    period, lag, difference, frequency)
                self.assertLess(abs(factored - direct), 1e-10)

    def test_source_reduction_reconstructs_leading_lag_mean(self):
        receipt = source_ramanujan_mean_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["gcd_lag_period"], 182)
        self.assertEqual(receipt["quotient_period"], 55)
        self.assertEqual(receipt["unit_class_count"], 2880)
        self.assertEqual(receipt["left_source_pair_count"], 5760)
        self.assertEqual(receipt["right_source_pair_count"], 5760)
        self.assertLess(receipt["source_to_canonical_relative_error"], 1e-12)
        self.assertTrue(receipt["source_term_ramanujan_reduction_proved"])
        self.assertEqual(
            tuple(receipt["prime_frequency_mean_correlations"]), (2, 7, 13))
        self.assertAlmostEqual(
            receipt["prime_frequency_signed_real_fractions"][7],
            receipt["factor_seven_signed_real_fraction"])
        self.assertAlmostEqual(
            receipt["factor_seven_frequency_mean_correlation"][0],
            -23978.413495740802, places=7)
        self.assertAlmostEqual(
            receipt["factor_seven_signed_real_fraction"],
            .9575124092409204, places=12)
        self.assertEqual(
            receipt["minimum_factor_seven_signed_fraction"], .75)
        self.assertTrue(receipt["factor_seven_signed_fraction_passes"])
        self.assertGreater(
            receipt["prime_frequency_signed_real_fractions"][13],
            receipt["factor_seven_signed_real_fraction"])
        allocations = receipt["frequency_equal_share_mean_correlations"]
        self.assertAlmostEqual(allocations[2][0], -3387.3799587328717, places=7)
        self.assertAlmostEqual(allocations[7][0], -10533.888282760554, places=7)
        self.assertAlmostEqual(allocations[13][0], -11122.65510486987, places=7)
        self.assertLess(
            receipt["equal_share_reconstruction_relative_error"], 1e-12)
        self.assertEqual(
            receipt["largest_absolute_equal_share_prime"], 13)
        self.assertFalse(
            receipt["factor_seven_has_largest_absolute_equal_share"])
        gcd_total = sum(
            complex(*subtotal) for subtotal in
            receipt["frequency_gcd_mean_correlations"].values())
        self.assertLess(abs(
            gcd_total
            - complex(*receipt["source_ramanujan_mean_correlation"])), 1e-9)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            source_ramanujan_mean_receipt(lag=0)
        with self.assertRaises(ValueError):
            _conditioned_unit_exponential_sum(12, 6, 6, 1)
        with self.assertRaises(ValueError):
            source_ramanujan_mean_receipt(
                minimum_factor_seven_signed_fraction=0)


if __name__ == "__main__":
    unittest.main()
