import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_m353_full_prime_sweep import (
    CHECKPOINT,
    PRIOR_STRESS_PRIMES,
    SCALE_MODULUS,
    m353_prime_moduli,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-m353-full-prime-sweep.json")


class MobiusMomentSquareDegree5SourceStartM353FullPrimeSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_prime_selector_is_deterministic(self):
        self.assertEqual(
            m353_prime_moduli(),
            [
                353, 359, 367, 373, 379, 383, 389, 397,
                401, 409, 419, 421, 431, 433, 439, 443,
                449, 457, 461, 463, 467, 479, 487, 491,
                499, 503, 509, 521, 523, 541, 547, 557,
                563, 569, 571, 577, 587, 593, 599, 601,
                607, 613, 617, 619, 631, 641, 643, 647,
                653, 659, 661, 673, 677, 683, 691, 701,
            ])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_source_start_m353_full_prime_rows")
        self.assertEqual(self.receipt["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(
            self.receipt["prior_stress_primes"], list(PRIOR_STRESS_PRIMES))
        self.assertTrue(self.receipt["one_full_fresh_scale_sweep_only"])
        self.assertTrue(self.receipt["finite_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertTrue(self.receipt["full_sweep_completed"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["prime_block_theorem_proved"])

    def test_prime_rows_cover_full_m353_interval(self):
        self.assertEqual(self.receipt["prime_interval"], [353, 706])
        self.assertEqual(self.receipt["prime_row_count"], 56)
        self.assertEqual(
            self.receipt["scale_result"]["prime_moduli"],
            m353_prime_moduli())

    def test_all_m353_prime_rows_pass(self):
        self.assertEqual(self.receipt["component_row_count"], 168)
        self.assertEqual(self.receipt["degree5_total_row_count"], 56)
        self.assertEqual(self.receipt["dominance_row_count"], 224)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 224, "zero": 0, "negative": 0})

    def test_prime_block_morphology_survives(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(weakest["prime_modulus"], 599)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9109632447421941)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.41096324474219414)
        self.assertTrue(self.receipt["top_four_rows_form_single_prime_block"])
        self.assertEqual(self.receipt["top_four_prime_modulus"], 599)
        self.assertEqual(
            set(self.receipt["top_four_labels"]),
            {"00,12", "01,02", "01,11", "TOTAL"})
        self.assertEqual(
            self.receipt["tightest_prime_blocks"][0]["prime_modulus"], 599)

    def test_prior_stress_prime_diagnostics(self):
        prior = self.receipt["prior_stress_prime_weakest_rows"]
        self.assertEqual(set(prior), {"379", "461", "599", "647"})
        self.assertAlmostEqual(
            prior["599"]["dominance_slack_above_one_half"],
            self.receipt["minimum_dominance_slack_above_one_half"])
        self.assertGreater(
            prior["647"]["dominance_slack_above_one_half"],
            self.receipt["minimum_dominance_slack_above_one_half"])
        self.assertGreater(
            prior["379"]["dominance_slack_above_one_half"],
            self.receipt["minimum_dominance_slack_above_one_half"])

    def test_resumable_runner_finished_cleanly(self):
        self.assertTrue(self.receipt["resumable_runner_used"])
        self.assertTrue(self.receipt["checkpoint_removed_after_success"])
        self.assertFalse(CHECKPOINT.exists())
        self.assertGreater(self.receipt["total_elapsed_seconds"], 100.0)
        self.assertEqual(
            len(self.receipt["scale_result"]["row_elapsed_seconds"]), 56)


if __name__ == "__main__":
    unittest.main()
