import unittest

from tools.build_mobius_positive_range_lower_frame_axial_falsifier import (
    build_receipt,
)


class MobiusPositiveRangeLowerFrameAxialFalsifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_receipt_preserves_proof_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "FALSIFY_axial_schur_compression_as_standalone_certificate__"
            "TARGET_positive_range_active_full_lower_frame")
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["q286_reactivated"])
        self.assertFalse(
            self.receipt["mobius_covariance_theorem_proved"])
        self.assertFalse(
            self.receipt["uniform_active_full_lower_frame_proved"])
        self.assertFalse(self.receipt["signed_prime_correlation_proved"])

    def test_positive_range_survives_checked_nonvacuous_scales(self):
        self.assertEqual(
            self.receipt["positive_range_nonvacuous_scales"],
            (127, 149, 167, 191))
        self.assertTrue(
            self.receipt[
                "positive_range_one_half_survives_checked_nonvacuous_scales"])
        self.assertAlmostEqual(
            self.receipt["positive_range_minimum_checked_eigenvalue"],
            0.8511480691308368)
        rows = {
            row["scale_modulus"]: row
            for row in self.receipt["positive_range_results"]}
        self.assertEqual(rows[167]["full_denominator_rank"], 5)
        self.assertEqual(rows[167]["full_denominator_nullity"], 1)
        self.assertFalse(
            rows[167]["active_positive_full_null_direction"])

    def test_full_pd_whitening_is_too_strong(self):
        self.assertTrue(
            self.receipt[
                "full_pd_whitening_acceptance_condition_falsified_on_checked_scales"])
        self.assertEqual(
            self.receipt["full_pd_whitening_failure_scales"],
            (83, 101, 167))
        failures = {
            row["scale_modulus"]: row
            for row in self.receipt[
                "full_pd_whitened_gershgorin_results"]
            if not row["ok"]}
        self.assertEqual(
            failures[83]["exception_message"],
            "full matrix must have a positive diagonal")
        self.assertEqual(
            failures[167]["exception_message"],
            "full matrix must be positive definite")

    def test_axial_compression_is_not_standalone_certificate(self):
        self.assertTrue(
            self.receipt[
                "axial_standalone_certificate_falsified_on_checked_scales"])
        self.assertEqual(
            self.receipt["axial_failure_scales"],
            (149, 167, 191))
        self.assertGreater(
            self.receipt["largest_nonaxial_error_over_schur_margin"],
            15.0)
        axial = {
            row["scale_modulus"]: row
            for row in self.receipt["axial_schur_results"]}
        self.assertLess(
            axial[149]["moment_curve_projective_distance"],
            3e-5)
        self.assertGreater(
            axial[149]["nonaxial_error_over_schur_margin"],
            2.9)


if __name__ == "__main__":
    unittest.main()
