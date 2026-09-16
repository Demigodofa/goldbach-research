import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_m383_full_prime_sweep import (
    CHECKPOINT,
    SCALE_MODULUS,
    m383_prime_moduli,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-m383-full-prime-sweep.json")


class MobiusMomentSquareDegree5SourceStartM383FullPrimeSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_prime_selector_is_deterministic(self):
        self.assertEqual(self.receipt["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(self.receipt["prime_interval"], [383, 766])
        self.assertEqual(self.receipt["scale_result"]["prime_moduli"],
                         m383_prime_moduli())
        self.assertEqual(len(m383_prime_moduli()), 60)
        self.assertEqual(m383_prime_moduli()[0], 383)
        self.assertEqual(m383_prime_moduli()[-1], 761)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_source_start_m383_full_prime_rows")
        self.assertTrue(self.receipt["one_full_fresh_scale_sweep_only"])
        self.assertTrue(self.receipt["finite_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertTrue(self.receipt["full_sweep_completed"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["prime_block_theorem_proved"])
        self.assertFalse(self.receipt["clearance_family_theorem_proved"])

    def test_row_counts_and_signs_are_self_consistent(self):
        self.assertEqual(self.receipt["prime_row_count"], 60)
        self.assertEqual(self.receipt["component_row_count"], 180)
        self.assertEqual(self.receipt["degree5_total_row_count"], 60)
        self.assertEqual(self.receipt["dominance_row_count"], 240)
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"]["positive"],
            240)
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"]["negative"],
            0)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])

    def test_tightest_block_preserves_morphology(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["prime_modulus"], 599)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"], 0.9215742230435717)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.4215742230435717)
        self.assertTrue(self.receipt["top_four_rows_form_single_prime_block"])
        self.assertEqual(self.receipt["top_four_prime_modulus"], 599)
        self.assertEqual(
            self.receipt["top_four_labels"],
            ["00,12", "TOTAL", "01,11", "01,02"])
        self.assertTrue(
            self.receipt["top_four_labels_match_component_total_block"])
        self.assertEqual(
            self.receipt["tightest_prime_blocks"][0]["prime_modulus"], 599)
        self.assertEqual(
            self.receipt["tightest_prime_blocks"][1]["prime_modulus"], 691)

    def test_resumable_runner_finished_cleanly(self):
        self.assertTrue(self.receipt["resumable_runner_used"])
        self.assertTrue(self.receipt["checkpoint_removed_after_success"])
        self.assertFalse(CHECKPOINT.exists())
        self.assertGreater(self.receipt["total_elapsed_seconds"], 0.0)
        self.assertEqual(
            len(self.receipt["scale_result"]["row_elapsed_seconds"]), 60)


if __name__ == "__main__":
    unittest.main()
