import unittest

import numpy as np

from tools.build_mobius_moment_square_coefficient_provenance_audit import (
    degree_contributions,
    sign_name,
    build_receipt,
)


class MobiusMomentSquareCoefficientProvenanceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_sign_name(self):
        self.assertEqual(sign_name(2.0), "positive")
        self.assertEqual(sign_name(-2.0), "negative")
        self.assertEqual(sign_name(0.0), "zero")
        self.assertEqual(sign_name(1e-3, tolerance=1e-2), "zero")

    def test_degree_contributions_match_direct_polynomial_coefficients(self):
        active = np.diag((17.0, 13.0, 11.0, 7.0, 5.0, 3.0))
        full = np.diag((2.0, 4.0, 6.0, 8.0, 10.0, 12.0))
        rows = degree_contributions(active, full)
        by_degree = {
            row["degree"]: row["half_frame_coefficient"] for row in rows}
        self.assertEqual(by_degree[8], 16.0)
        self.assertEqual(by_degree[6], 11.0)
        self.assertEqual(by_degree[4], 11.0)
        self.assertEqual(by_degree[2], 0.0)
        self.assertEqual(by_degree[0], -3.0)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "TARGET_moment_square_coefficient_provenance")
        self.assertTrue(
            self.receipt["finite_coefficient_provenance_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["coefficient_family_theorem_proved"])
        self.assertFalse(
            self.receipt["universal_sturm_certificate_theorem_proved"])

    def test_checked_coefficients_match_source_and_stable_pattern(self):
        self.assertTrue(
            self.receipt["all_reconstructed_coefficients_match_source"])
        self.assertLess(
            self.receipt["maximum_relative_source_coefficient_delta"],
            1e-12)
        self.assertTrue(
            self.receipt["all_alternating_degree_sign_patterns_hold"])
        self.assertTrue(
            self.receipt["stable_top_abs_contributor_signature"])
        signature = self.receipt["top_abs_contributor_signature"]
        self.assertEqual(signature[0], (0, "22", "22"))
        self.assertEqual(signature[8], (8, "00", "00"))


if __name__ == "__main__":
    unittest.main()
