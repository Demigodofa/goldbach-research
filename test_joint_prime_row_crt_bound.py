import math
import unittest

import numpy as np

from joint_prime_row_crt_bound import (
    endpoint_fourier_coefficient_bound,
    exact_rotation_second_moment,
    incomplete_rotation_second_moment_bound,
    joint_prime_row_phase_envelope,
    project_endpoint_exponent_budget,
    row_geometric_sum,
)
from signed_crt_discrepancy_probe import crt_interval_count_error


class JointPrimeRowCrtBoundTests(unittest.TestCase):
    def test_endpoint_interval_fourier_coefficients_obey_majorant(self):
        for period in range(2, 41):
            for length in range(1, 2 * period + 1):
                values = np.array([
                    crt_interval_count_error(
                        1, length, residue, period)[2]
                    for residue in range(period)])
                coefficients = np.fft.fft(values) / period
                self.assertAlmostEqual(coefficients[0].real, 0, places=12)
                for frequency in range(1, period):
                    self.assertLessEqual(
                        abs(coefficients[frequency]),
                        endpoint_fourier_coefficient_bound(
                            period, frequency) + 1e-12)

    def test_complete_rotation_orthogonality_identity(self):
        for period in (5, 12, 35):
            for frequency in range(1, period):
                for row_first, row_count in ((0, 3), (2, 7), (5, 19)):
                    receipt = exact_rotation_second_moment(
                        period, frequency, row_first, row_count)
                    self.assertAlmostEqual(
                        receipt["exact_second_moment"],
                        receipt["orthogonality_value"], places=8)
                    self.assertLessEqual(
                        receipt["orthogonality_value"],
                        receipt["upper_bound"])

    def test_incomplete_bound_dominates_every_start(self):
        for period, frequency in ((12, 4), (35, 6), (35, 14)):
            for modulus_count, row_count in ((3, 8), (17, 9), (51, 22)):
                bound = incomplete_rotation_second_moment_bound(
                    period, frequency, modulus_count, row_count)
                rotation = period // math.gcd(period, frequency)
                for start in range(rotation):
                    direct = sum(abs(row_geometric_sum(
                        period, frequency, multiplier, 4, row_count)) ** 2
                        for multiplier in range(start, start + modulus_count))
                    self.assertLessEqual(direct, bound + 1e-8)

    def test_prime_subset_cauchy_envelope_is_valid(self):
        period, modulus_count, row_count = 35, 51, 22
        subset = (1, 3, 7, 12, 19, 24, 31, 42)
        direct = 0.0
        for frequency in range(1, period):
            coefficient = 1 / (2 * min(frequency, period - frequency))
            direct += coefficient * sum(abs(row_geometric_sum(
                period, frequency, multiplier, 4, row_count))
                for multiplier in subset)
        receipt = joint_prime_row_phase_envelope(
            period, modulus_count, row_count, len(subset))
        self.assertLessEqual(
            direct, receipt["proved_fourier_cauchy_envelope"] + 1e-8)
        self.assertTrue(receipt["joint_prime_row_phase_bound_proved"])

    def test_project_thresholds_preserve_strict_endpoints(self):
        old_endpoint = project_endpoint_exponent_budget(.245)
        extended = project_endpoint_exponent_budget(.294)
        frame_endpoint = project_endpoint_exponent_budget(.295)
        active_endpoint = project_endpoint_exponent_budget(49 / 150)
        self.assertEqual(
            old_endpoint["absolute_single_row_endpoint_exponent"], 0)
        self.assertTrue(extended["assembled_lower_union_supported"])
        self.assertFalse(frame_endpoint["exact_full_frame_power_saving"])
        self.assertFalse(active_endpoint["joint_endpoint_power_saving"])
        self.assertAlmostEqual(
            extended["joint_endpoint_worst_exponent"], -.049, places=12)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            joint_prime_row_phase_envelope(1, 10, 4, 2)
        with self.assertRaises(ValueError):
            project_endpoint_exponent_budget(.5)


if __name__ == "__main__":
    unittest.main()
