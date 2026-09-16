import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_m251_full_prime_sweep import (
    SCALE_MODULUS,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-m251-full-prime-sweep.json")


class MobiusMomentSquareDegree5SourceStartM251FullPrimeSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_source_start_m251_full_prime_rows")
        self.assertEqual(self.receipt["scale_modulus"], SCALE_MODULUS)
        self.assertTrue(self.receipt["one_full_fresh_scale_sweep_only"])
        self.assertTrue(self.receipt["finite_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["all_fresh_scales_swept"])

    def test_prime_rows_cover_full_m251_interval(self):
        self.assertEqual(self.receipt["prime_interval"], [251, 502])
        self.assertEqual(self.receipt["prime_row_count"], 42)
        self.assertEqual(
            self.receipt["scale_result"]["prime_moduli"],
            [
                251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
                311, 313, 317, 331, 337, 347, 349, 353, 359, 367,
                373, 379, 383, 389, 397, 401, 409, 419, 421, 431,
                433, 439, 443, 449, 457, 461, 463, 467, 479, 487,
                491, 499,
            ])

    def test_all_m251_prime_rows_pass(self):
        self.assertEqual(self.receipt["component_row_count"], 126)
        self.assertEqual(self.receipt["degree5_total_row_count"], 42)
        self.assertEqual(self.receipt["dominance_row_count"], 168)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 168, "zero": 0, "negative": 0})

    def test_weakest_row_repeats_prime_379_attention_point(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 251)
        self.assertEqual(weakest["prime_modulus"], 379)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.934353336374303)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.43435333637430296)


if __name__ == "__main__":
    unittest.main()
