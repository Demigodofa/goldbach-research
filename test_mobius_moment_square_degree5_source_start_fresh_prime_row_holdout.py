import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_fresh_prime_row_holdout import (
    FRESH_SCALES,
    first_prime_at_or_above,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-fresh-prime-row-holdout.json")


class MobiusMomentSquareDegree5SourceStartFreshPrimeRowHoldoutTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_first_prime_selector_is_deterministic(self):
        self.assertEqual(first_prime_at_or_above(229), 229)
        self.assertEqual(first_prime_at_or_above(230), 233)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "HOLDOUT_degree5_source_start_fresh_first_prime_rows")
        self.assertTrue(self.receipt["fresh_first_prime_row_holdout_only"])
        self.assertFalse(self.receipt["full_fresh_scale_sweep_completed"])
        self.assertTrue(self.receipt["finite_holdout_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])

    def test_holdout_uses_fresh_scales_only(self):
        self.assertEqual(self.receipt["fresh_scales"], list(FRESH_SCALES))
        self.assertEqual(self.receipt["fresh_scale_count"], 3)
        self.assertEqual(self.receipt["prime_row_count"], 3)
        for scale_row in self.receipt["scale_results"]:
            self.assertGreater(scale_row["scale_modulus"], 227)
            self.assertEqual(
                scale_row["canonical_source_start"],
                scale_row["row_count"])
            self.assertEqual(
                scale_row["scale_modulus"], scale_row["prime_modulus"])

    def test_all_fresh_first_prime_rows_pass(self):
        self.assertEqual(self.receipt["component_row_count"], 9)
        self.assertEqual(self.receipt["degree5_total_row_count"], 3)
        self.assertEqual(self.receipt["dominance_row_count"], 12)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 12, "zero": 0, "negative": 0})
        self.assertGreater(
            self.receipt["minimum_dominance_slack_above_one_half"], 0.0)

    def test_weakest_row_is_recorded(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 251)
        self.assertEqual(weakest["prime_modulus"], 251)
        self.assertEqual(weakest["label"], "01,02")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9959390121702468)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.49593901217024683)


if __name__ == "__main__":
    unittest.main()
