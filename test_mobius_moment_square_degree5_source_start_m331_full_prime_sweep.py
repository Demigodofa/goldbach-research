import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_m331_full_prime_sweep import (
    ATTENTION_PRIME,
    CHECKPOINT,
    SCALE_MODULUS,
    m331_prime_moduli,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-m331-full-prime-sweep.json")


class MobiusMomentSquareDegree5SourceStartM331FullPrimeSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_prime_selector_is_deterministic(self):
        self.assertEqual(
            m331_prime_moduli(),
            [
                331, 337, 347, 349, 353, 359, 367, 373, 379,
                383, 389, 397, 401, 409, 419, 421, 431, 433,
                439, 443, 449, 457, 461, 463, 467, 479, 487,
                491, 499, 503, 509, 521, 523, 541, 547, 557,
                563, 569, 571, 577, 587, 593, 599, 601, 607,
                613, 617, 619, 631, 641, 643, 647, 653, 659,
                661,
            ])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_source_start_m331_full_prime_rows")
        self.assertEqual(self.receipt["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(self.receipt["attention_prime"], ATTENTION_PRIME)
        self.assertTrue(self.receipt["one_full_fresh_scale_sweep_only"])
        self.assertTrue(self.receipt["finite_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertTrue(self.receipt["full_sweep_completed"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["all_fresh_scales_swept"])

    def test_prime_rows_cover_full_m331_interval(self):
        self.assertEqual(self.receipt["prime_interval"], [331, 662])
        self.assertEqual(self.receipt["prime_row_count"], 55)
        self.assertEqual(
            self.receipt["scale_result"]["prime_moduli"],
            m331_prime_moduli())

    def test_all_m331_prime_rows_pass(self):
        self.assertEqual(self.receipt["component_row_count"], 165)
        self.assertEqual(self.receipt["degree5_total_row_count"], 55)
        self.assertEqual(self.receipt["dominance_row_count"], 220)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 220, "zero": 0, "negative": 0})

    def test_full_sweep_downgrades_attention_prime(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(weakest["prime_modulus"], 599)
        self.assertEqual(weakest["label"], "00,12")
        self.assertFalse(self.receipt["weakest_prime_equals_attention_prime"])
        self.assertEqual(
            self.receipt["weakest_prime_distance_from_attention_prime"], 138)
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9047925604770473)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.40479256047704726)
        attention = self.receipt["attention_prime_weakest_row"]
        self.assertEqual(attention["prime_modulus"], ATTENTION_PRIME)
        self.assertGreater(
            attention["dominance_slack_above_one_half"],
            weakest["dominance_slack_above_one_half"])
        self.assertAlmostEqual(
            attention["dominance_slack_above_one_half"],
            0.4702648688514812)

    def test_resumable_runner_finished_cleanly(self):
        self.assertTrue(self.receipt["resumable_runner_used"])
        self.assertTrue(self.receipt["checkpoint_removed_after_success"])
        self.assertFalse(CHECKPOINT.exists())
        self.assertGreater(self.receipt["total_elapsed_seconds"], 100.0)
        self.assertEqual(
            len(self.receipt["scale_result"]["row_elapsed_seconds"]), 55)


if __name__ == "__main__":
    unittest.main()
