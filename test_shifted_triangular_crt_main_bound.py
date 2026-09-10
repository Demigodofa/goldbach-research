import unittest

from near_cutoff_geometric_bound import _active_modes
from shifted_triangular_crt_main_bound import (
    row_shifted_triangular_main_bound,
    shifted_kernel_active_sum_bound,
    shifted_triangular_feature_kernel,
    shifted_triangular_kernel,
)


class ShiftedTriangularCrtMainBoundTests(unittest.TestCase):
    def test_cross_correlation_identity_and_pointwise_domination(self):
        modulus = 101
        for gcd_value in (2, 5, 14):
            zero_values = {}
            for frequency in range(1, modulus):
                zero_values[frequency] = shifted_triangular_kernel(
                    modulus, gcd_value, 0, frequency)
            for residue in range(gcd_value):
                for frequency in range(1, modulus):
                    direct = shifted_triangular_kernel(
                        modulus, gcd_value, residue, frequency)
                    feature = shifted_triangular_feature_kernel(
                        modulus, gcd_value, residue, frequency)
                    self.assertAlmostEqual(direct.real, feature.real, places=8)
                    self.assertAlmostEqual(direct.imag, feature.imag, places=8)
                    self.assertLessEqual(
                        abs(direct), zero_values[frequency].real + 1e-8)

    def test_active_sum_is_below_inherited_bound(self):
        modulus, shift_length, gcd_value, row_delta = 1009, 5, 14, 7
        residue = modulus * row_delta % gcd_value
        exact = sum(abs(shifted_triangular_kernel(
            modulus, gcd_value, residue, frequency))
            for frequency in _active_modes(modulus, shift_length))
        proved = shifted_kernel_active_sum_bound(
            modulus, shift_length, gcd_value, row_delta)
        self.assertLessEqual(
            exact, proved["proved_absolute_active_kernel_sum_bound"] + 1e-6)

    def test_row_bound_is_uniform_in_delta(self):
        zero = row_shifted_triangular_main_bound(1009, 5, 8, 0)
        shifted = row_shifted_triangular_main_bound(1009, 5, 8, 37)
        self.assertEqual(
            zero["proved_triangular_main_schur_bound"],
            shifted["proved_triangular_main_schur_bound"])
        self.assertTrue(shifted["shifted_triangular_main_bound_proved"])
        self.assertFalse(shifted["shifted_discrepancy_proved"])

    def test_composite_modulus_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            shifted_kernel_active_sum_bound(1001, 5, 14, 7)


if __name__ == "__main__":
    unittest.main()
