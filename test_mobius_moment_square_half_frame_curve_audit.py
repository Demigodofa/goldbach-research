import unittest

import numpy as np

from tools.build_mobius_moment_square_half_frame_curve_audit import (
    build_receipt,
    moment_square_quadratic_polynomial,
    polynomial_minimum,
)


class MobiusMomentSquareHalfFrameCurveAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_polynomial_helper_recovers_diagonal_terms(self):
        matrix = np.diag((2.0, 3.0, 0.0, 5.0, 7.0, 11.0))
        polynomial = moment_square_quadratic_polynomial(matrix)
        self.assertAlmostEqual(polynomial(2.0), 2 * 2.0 ** 8
                               + 3 * 2.0 ** 6
                               + 5 * 2.0 ** 4
                               + 7 * 2.0 ** 2
                               + 11)

    def test_polynomial_minimum_finds_real_minimum(self):
        polynomial = (PolynomialForTest.shifted_square(.25)
                      + PolynomialForTest.constant(3.0))
        receipt = polynomial_minimum(polynomial)
        self.assertAlmostEqual(receipt["minimum_value"], 3.0)
        self.assertAlmostEqual(receipt["minimizing_parameter"], .25)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "TARGET_moment_square_half_frame_curve_positivity")
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt[
                "moment_square_half_frame_curve_positivity_theorem_proved"])
        self.assertFalse(
            self.receipt["uniform_active_full_lower_frame_proved"])

    def test_checked_curve_minima_are_positive(self):
        self.assertTrue(
            self.receipt["all_half_frame_curve_minima_positive"])
        self.assertGreater(
            self.receipt["minimum_half_frame_curve_value"], 0.42)
        self.assertLess(
            self.receipt["minimum_half_frame_curve_value"], 0.43)
        weakest = self.receipt["weakest_half_frame_curve_row"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertAlmostEqual(
            weakest["half_frame_curve_minimizing_parameter"],
            0.26983489124712867)
        self.assertEqual(weakest["half_frame_curve_degree"], 8)
        self.assertGreater(
            weakest["half_frame_curve_leading_coefficient"], 0.0)


class PolynomialForTest:
    @staticmethod
    def constant(value):
        from numpy.polynomial import Polynomial

        return Polynomial((value,))

    @staticmethod
    def shifted_square(center):
        from numpy.polynomial import Polynomial

        variable = Polynomial((0.0, 1.0))
        return (variable - center) ** 2


if __name__ == "__main__":
    unittest.main()
