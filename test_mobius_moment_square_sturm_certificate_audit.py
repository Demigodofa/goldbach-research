import unittest

import sympy as sp

from tools.build_mobius_moment_square_sturm_certificate_audit import (
    build_receipt,
    rational_polynomial,
    sturm_certificate_row,
)


class MobiusMomentSquareSturmCertificateAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_rational_polynomial_uses_decimal_coefficients_exactly(self):
        variable = sp.symbols("t")
        polynomial = rational_polynomial(["1.25", "-0.5", "3"], variable)
        self.assertEqual(polynomial.domain, sp.QQ)
        self.assertEqual(polynomial.eval(2), sp.Rational(49, 4))

    def test_sturm_row_detects_failing_shifted_polynomial(self):
        row = {
            "scale_modulus": 1,
            "polynomial_coefficients_low_to_high": [1.0, 0.0, 1.0],
            "half_frame_curve_minimum": 1.0,
            "half_frame_curve_minimizing_parameter": 0.0,
        }
        certificate = sturm_certificate_row(row, margin=sp.Rational(2, 1))
        self.assertEqual(
            certificate["shifted_polynomial_real_root_count"], 2)
        self.assertFalse(certificate["certificate_passes"])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "CERTIFY_checked_moment_square_half_frame_curve_margin")
        self.assertTrue(
            self.receipt["finite_polynomial_certificate_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["universal_sturm_certificate_theorem_proved"])
        self.assertFalse(
            self.receipt[
                "moment_square_half_frame_curve_positivity_theorem_proved"])

    def test_checked_polynomials_have_sturm_margin_certificate(self):
        self.assertAlmostEqual(self.receipt["certified_margin"], 0.427)
        self.assertTrue(self.receipt["all_shifted_polynomials_root_free"])
        self.assertTrue(self.receipt["all_certificates_pass"])
        rows = {
            row["scale_modulus"]: row
            for row in self.receipt["scale_results"]}
        self.assertEqual(
            rows[167]["shifted_polynomial_real_root_count"], 0)
        self.assertTrue(
            rows[167]["shifted_polynomial_leading_coefficient_positive"])
        self.assertTrue(
            rows[167]["shifted_polynomial_value_at_zero_positive"])
        self.assertEqual(
            self.receipt["weakest_source_curve_row"]["scale_modulus"],
            167)


if __name__ == "__main__":
    unittest.main()
