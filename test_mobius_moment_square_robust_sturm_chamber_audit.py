import unittest

from tools.build_mobius_moment_square_robust_sturm_chamber_audit import (
    build_receipt,
    sturm_signature,
    variation_count,
)


class MobiusMomentSquareRobustSturmChamberAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_variation_count_ignores_zero_signs(self):
        self.assertEqual(variation_count("++--"), 1)
        self.assertEqual(variation_count("+0-0+"), 2)

    def test_sturm_signature_records_root_count_from_variations(self):
        signature = sturm_signature([1.0, 0.0, 1.0], margin=0)
        self.assertEqual(signature["real_root_count_from_variations"], 0)
        failing = sturm_signature([1.0, 0.0, 1.0], margin=2)
        self.assertEqual(failing["real_root_count_from_variations"], 2)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "TARGET_robust_sturm_variation_chamber")
        self.assertTrue(
            self.receipt["finite_sturm_chamber_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["robust_sturm_variation_chamber_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_checked_chamber_variations_pass_for_both_serializations(self):
        self.assertEqual(self.receipt["robust_margin_rational"], "21/50")
        self.assertTrue(
            self.receipt["all_source_and_provenance_sign_words_match"])
        self.assertTrue(
            self.receipt["all_source_and_provenance_variations_match"])
        self.assertTrue(
            self.receipt["all_source_variation_certificates_pass"])
        self.assertTrue(
            self.receipt["all_provenance_variation_certificates_pass"])
        for row in self.receipt["scale_results"]:
            self.assertEqual(
                row["source_signature"]["plus_infinity_variations"], 4)
            self.assertEqual(
                row["source_signature"]["minus_infinity_variations"], 4)
            self.assertEqual(
                row["source_signature"]["real_root_count_from_variations"],
                0)

    def test_sign_word_is_not_single_global_target(self):
        self.assertGreater(
            self.receipt["distinct_checked_sign_word_pair_count"], 1)


if __name__ == "__main__":
    unittest.main()
