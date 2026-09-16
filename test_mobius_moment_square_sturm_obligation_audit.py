import unittest

from tools.build_mobius_moment_square_sturm_obligation_audit import (
    build_receipt,
    sturm_obligations_for_coefficients,
    variation_count,
)


class MobiusMomentSquareSturmObligationAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_variation_count_ignores_zero_signs(self):
        self.assertEqual(variation_count("+0-0+"), 2)
        self.assertEqual(variation_count("++--"), 1)

    def test_obligation_helper_detects_roots_after_large_shift(self):
        passing = sturm_obligations_for_coefficients([1.0, 0.0, 1.0], 0)
        self.assertEqual(passing["real_root_count_from_variations"], 0)
        failing = sturm_obligations_for_coefficients([1.0, 0.0, 1.0], 2)
        self.assertEqual(failing["real_root_count_from_variations"], 2)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "EXTRACT_robust_sturm_sign_obligations")
        self.assertTrue(
            self.receipt["finite_sturm_obligation_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["sturm_obligation_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_checked_obligations_have_no_zero_leading_coefficients(self):
        self.assertEqual(
            self.receipt["zero_leading_coefficient_obligation_count"], 0)
        self.assertTrue(
            self.receipt["all_source_variation_certificates_pass"])
        self.assertTrue(
            self.receipt["all_provenance_variation_certificates_pass"])
        for row in self.receipt["scale_results"]:
            self.assertEqual(
                row["source_curve_serialized"][
                    "real_root_count_from_variations"], 0)
            self.assertEqual(
                row["coefficient_provenance_serialized"][
                    "real_root_count_from_variations"], 0)

    def test_source_and_provenance_share_checked_sign_words(self):
        self.assertTrue(
            self.receipt["all_source_and_provenance_sign_words_match"])
        self.assertTrue(
            self.receipt[
                "all_source_and_provenance_variation_counts_match"])
        self.assertEqual(
            self.receipt["distinct_checked_sign_word_pair_count"], 4)

    def test_weakest_obligation_is_m167_terminal_sturm_constant(self):
        weakest = self.receipt["weakest_checked_leading_obligation"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertEqual(
            weakest["coefficient_family"],
            "coefficient_provenance_serialized")
        self.assertEqual(weakest["sequence_index"], 8)
        self.assertEqual(weakest["degree"], 0)
        self.assertEqual(weakest["leading_coefficient_sign"], "+")
        self.assertLess(weakest["leading_coefficient_abs_log10"], -18)


if __name__ == "__main__":
    unittest.main()
