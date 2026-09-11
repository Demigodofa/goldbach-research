import math
import unittest

import numpy as np

from lcm_sawtooth_source_ramanujan import (
    _conditioned_unit_exponential_sum,
    _endpoint_modes,
    leading_lag_source_receipt,
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
        self.assertGreater(
            receipt["normalized_absolute_mode_contribution_mass"],
            abs(complex(*receipt["source_ramanujan_mean_correlation"])))
        self.assertEqual(
            receipt["maximum_source_mode_cancellation_quotient"], .10)
        self.assertAlmostEqual(
            receipt["normalized_absolute_mode_contribution_mass"],
            392973.25954838906, places=6)
        self.assertAlmostEqual(
            receipt["source_mode_cancellation_quotient"],
            .06382956757596069, places=12)
        self.assertTrue(receipt["source_mode_cancellation_gate_passes"])
        self.assertIsNotNone(receipt["phase_removed_cancellation_quotient"])
        self.assertAlmostEqual(
            receipt["phase_removed_source_mean_correlation"][0],
            207647 / 60, places=8)
        self.assertAlmostEqual(
            receipt["phase_removed_source_mean_correlation"][1], 0, places=8)
        self.assertAlmostEqual(
            receipt["phase_removed_cancellation_quotient"],
            .00880666368319958, places=12)
        self.assertTrue(receipt["phase_removed_cancellation_gate_passes"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            source_ramanujan_mean_receipt(lag=0)
        with self.assertRaises(ValueError):
            _conditioned_unit_exponential_sum(12, 6, 6, 1)
        with self.assertRaises(ValueError):
            source_ramanujan_mean_receipt(
                minimum_factor_seven_signed_fraction=0)
        with self.assertRaises(ValueError):
            source_ramanujan_mean_receipt(
                maximum_source_mode_cancellation_quotient=0)

    def test_zero_mass_lag_has_no_cancellation_quotient(self):
        receipt = source_ramanujan_mean_receipt(
            lag=1, canonical_target=(0.0, 0.0))
        self.assertEqual(receipt["normalized_absolute_mode_contribution_mass"], 0)
        self.assertIsNone(receipt["source_mode_cancellation_quotient"])
        self.assertFalse(receipt["source_mode_cancellation_gate_passes"])
        self.assertIsNone(receipt["phase_removed_cancellation_quotient"])
        self.assertFalse(receipt["phase_removed_cancellation_gate_passes"])

    def test_source_reduction_across_five_leading_lags(self):
        receipt = leading_lag_source_receipt()
        self.assertEqual(receipt["lags"], (140, 154, 156, 182, 240))
        self.assertEqual(
            receipt["lag_gcds"],
            {140: 70, 154: 154, 156: 26, 182: 182, 240: 10})
        self.assertLess(
            receipt["maximum_source_to_canonical_relative_error"], 1e-12)
        self.assertTrue(receipt["all_leading_lag_source_reductions_pass"])
        expected_quotients = {
            140: .022079556630137137,
            154: .02041835507328635,
            156: .01237114100186055,
            182: .06382956757596069,
            240: .020494909233862327,
        }
        for lag, expected in expected_quotients.items():
            self.assertAlmostEqual(
                receipt["source_mode_cancellation_quotients"][lag],
                expected, places=12)
        self.assertAlmostEqual(
            receipt["maximum_source_mode_cancellation_quotient"],
            expected_quotients[182], places=12)
        self.assertTrue(receipt["all_source_mode_cancellation_gates_pass"])
        expected_phase_removed_means = {
            140: -85437 / 4,
            154: 20185 / 9,
            156: 12375 / 2,
            182: 207647 / 60,
            240: -27225 / 2,
        }
        expected_phase_removed_quotients = {
            140: .02851697183540638,
            154: .005374667734400949,
            156: .012539400592394204,
            182: .00880666368319958,
            240: .015052682132974667,
        }
        for lag in receipt["lags"]:
            phase_removed_mean = receipt[
                "phase_removed_source_mean_correlations"][lag]
            self.assertAlmostEqual(
                phase_removed_mean[0], expected_phase_removed_means[lag],
                places=8)
            self.assertAlmostEqual(phase_removed_mean[1], 0, places=8)
            self.assertAlmostEqual(
                receipt["phase_removed_cancellation_quotients"][lag],
                expected_phase_removed_quotients[lag], places=12)
        self.assertTrue(receipt["all_phase_removed_cancellation_gates_pass"])
        self.assertFalse(
            receipt["unit_frame_classes_enumerated_by_source_calculation"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
