import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_fresh_prime_span_holdout import (
    FRESH_SCALES,
    selected_prime_span,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-fresh-prime-span-holdout.json")


class MobiusMomentSquareDegree5SourceStartFreshPrimeSpanHoldoutTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_prime_span_selector_is_deterministic(self):
        self.assertEqual(
            selected_prime_span(229),
            [("low", 229), ("mid", 347), ("high", 457)])
        self.assertEqual(
            selected_prime_span(251),
            [("low", 251), ("mid", 373), ("high", 499)])
        self.assertEqual(
            selected_prime_span(293),
            [("low", 293), ("mid", 439), ("high", 577)])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "HOLDOUT_degree5_source_start_fresh_prime_span_rows")
        self.assertTrue(self.receipt["fresh_prime_span_holdout_only"])
        self.assertFalse(self.receipt["full_fresh_scale_sweep_completed"])
        self.assertTrue(self.receipt["finite_holdout_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])

    def test_holdout_uses_fresh_low_mid_high_rows(self):
        self.assertEqual(self.receipt["fresh_scales"], list(FRESH_SCALES))
        self.assertEqual(self.receipt["span_positions"], ["low", "mid", "high"])
        self.assertEqual(self.receipt["fresh_scale_count"], 3)
        self.assertEqual(self.receipt["prime_row_count"], 9)
        for scale_row in self.receipt["scale_results"]:
            self.assertGreater(scale_row["scale_modulus"], 227)
            self.assertEqual(scale_row["prime_row_count"], 3)
            self.assertEqual(
                [row["span_position"] for row in scale_row["selected_primes"]],
                ["low", "mid", "high"])
            for prime_row in scale_row["prime_rows"]:
                self.assertEqual(
                    prime_row["canonical_source_start"],
                    prime_row["row_count"])

    def test_all_fresh_prime_span_rows_pass(self):
        self.assertEqual(self.receipt["component_row_count"], 27)
        self.assertEqual(self.receipt["degree5_total_row_count"], 9)
        self.assertEqual(self.receipt["dominance_row_count"], 36)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 36, "zero": 0, "negative": 0})
        self.assertGreater(
            self.receipt["minimum_dominance_slack_above_one_half"], 0.0)

    def test_weakest_row_is_mid_scale_229_component(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 229)
        self.assertEqual(weakest["prime_modulus"], 347)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9412712796572614)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.44127127965726143)


if __name__ == "__main__":
    unittest.main()
