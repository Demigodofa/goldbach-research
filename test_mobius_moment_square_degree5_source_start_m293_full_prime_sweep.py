import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_m293_full_prime_sweep import (
    ATTENTION_PRIME,
    SCALE_MODULUS,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-m293-full-prime-sweep.json")


class MobiusMomentSquareDegree5SourceStartM293FullPrimeSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_source_start_m293_full_prime_rows")
        self.assertEqual(self.receipt["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(self.receipt["attention_prime"], ATTENTION_PRIME)
        self.assertTrue(self.receipt["one_full_fresh_scale_sweep_only"])
        self.assertTrue(self.receipt["finite_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["all_fresh_scales_swept"])

    def test_prime_rows_cover_full_m293_interval(self):
        self.assertEqual(self.receipt["prime_interval"], [293, 586])
        self.assertEqual(self.receipt["prime_row_count"], 45)
        self.assertEqual(
            self.receipt["scale_result"]["prime_moduli"],
            [
                293, 307, 311, 313, 317, 331, 337, 347, 349,
                353, 359, 367, 373, 379, 383, 389, 397, 401,
                409, 419, 421, 431, 433, 439, 443, 449, 457,
                461, 463, 467, 479, 487, 491, 499, 503, 509,
                521, 523, 541, 547, 557, 563, 569, 571, 577,
            ])

    def test_all_m293_prime_rows_pass(self):
        self.assertEqual(self.receipt["component_row_count"], 135)
        self.assertEqual(self.receipt["degree5_total_row_count"], 45)
        self.assertEqual(self.receipt["dominance_row_count"], 180)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 180, "zero": 0, "negative": 0})

    def test_weakest_row_downgrades_p379_attention_point(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 293)
        self.assertEqual(weakest["prime_modulus"], 461)
        self.assertEqual(weakest["label"], "00,12")
        self.assertFalse(self.receipt["weakest_prime_equals_attention_prime"])
        self.assertEqual(
            self.receipt["weakest_prime_distance_from_attention_prime"], 82)
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9257305726250574)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.4257305726250574)

    def test_attention_prime_still_passes_but_is_not_tightest(self):
        attention = self.receipt["attention_prime_weakest_row"]
        self.assertEqual(attention["prime_modulus"], ATTENTION_PRIME)
        self.assertEqual(attention["label"], "00,12")
        self.assertGreater(
            attention["dominance_slack_above_one_half"],
            self.receipt["minimum_dominance_slack_above_one_half"])
        self.assertAlmostEqual(
            attention["dominance_slack_above_one_half"],
            0.4715916000491919)


if __name__ == "__main__":
    unittest.main()
