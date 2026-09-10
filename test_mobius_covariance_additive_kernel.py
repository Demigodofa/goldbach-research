import cmath
import unittest
from math import pi

from mobius_band_character_covariance import active_nonzero_modes
from mobius_covariance_additive_kernel import (
    additive_band_transform,
    direct_off_covariance,
    kernel_off_covariance,
    mean_zero_off_covariance,
    off_covariance_decomposition,
    off_covariance_kernel,
)
from resonant_covariance_falsifier import resonant_covariance_receipt


class MobiusCovarianceAdditiveKernelTests(unittest.TestCase):
    def test_additive_kernel_equals_direct_band_minus_diagonal(self):
        coefficients = {1: 2 - 1j, 3: -0.5 + 0.25j, 8: 1.75j}
        direct = direct_off_covariance(11, 2, coefficients)
        kernel = kernel_off_covariance(11, 2, coefficients)
        self.assertAlmostEqual(direct.real, kernel.real, places=10)
        self.assertAlmostEqual(direct.imag, kernel.imag, places=10)
        self.assertAlmostEqual(kernel.imag, 0.0, places=10)

    def test_literal_diagonal_formula_and_trace_zero(self):
        prime, shift_length = 101, 3
        r = len(active_nonzero_modes(prime, shift_length))
        trace = 0j
        for x in range(1, prime):
            actual = off_covariance_kernel(prime, shift_length, x, x)
            closed = (2 * additive_band_transform(prime, shift_length, x)
                      / (prime - 1) + 2 * r / (prime - 1) ** 2)
            self.assertAlmostEqual(actual.real, closed.real, places=11)
            self.assertAlmostEqual(actual.imag, closed.imag, places=11)
            trace += actual
        self.assertAlmostEqual(trace.real, 0.0, places=10)
        self.assertAlmostEqual(trace.imag, 0.0, places=10)

    def test_resonance_is_recovered_from_off_diagonal_quadratic_form(self):
        prime, shift_length = 101, 3
        receipt = resonant_covariance_receipt(prime, shift_length)
        h0 = receipt["resonant_frequency"]
        coefficients = {a: cmath.exp(2j * pi * h0 * a / prime)
                        for a in range(1, prime)}
        actual = kernel_off_covariance(prime, shift_length, coefficients)
        self.assertAlmostEqual(actual.real,
                               float(receipt["off_diagonal_energy"]), places=7)
        self.assertAlmostEqual(actual.imag, 0.0, places=7)

    def test_decomposition_keeps_all_centering_terms(self):
        coefficients = {1: 2 - 1j, 3: -0.5 + 0.25j, 8: 1.75j}
        result = off_covariance_decomposition(11, 2, coefficients)
        recombined = (result["literal_diagonal"]
                      + result["leading_W_off_diagonal"]
                      + result["centering_off_diagonal"])
        self.assertAlmostEqual(result["total"].real, recombined.real, places=11)
        self.assertAlmostEqual(result["total"].imag, recombined.imag, places=11)
        self.assertGreater(abs(result["centering_off_diagonal"]), 0)

    def test_mean_zero_projection_removes_rank_terms_exactly(self):
        coefficients = {1: 2 - 1j, 3: -0.5 + 0.25j, 8: 1.75j}
        direct = direct_off_covariance(11, 2, coefficients)
        projected = mean_zero_off_covariance(11, 2, coefficients)
        self.assertAlmostEqual(sum(projected["discrepancies"]).real, 0.0,
                               places=12)
        self.assertAlmostEqual(sum(projected["discrepancies"]).imag, 0.0,
                               places=12)
        self.assertAlmostEqual(direct.real,
                               projected["off_diagonal"].real, places=10)
        self.assertAlmostEqual(direct.imag,
                               projected["off_diagonal"].imag, places=10)


if __name__ == "__main__":
    unittest.main()
