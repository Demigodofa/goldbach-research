import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_m331_sentinel_audit import (
    ATTENTION_PRIME,
    SCALE_MODULUS,
    selected_sentinel_primes,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-m331-sentinel-audit.json")


class MobiusMomentSquareDegree5SourceStartM331SentinelAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_sentinel_selector_is_deterministic(self):
        self.assertEqual(
            selected_sentinel_primes(),
            [("low", 331), ("attention", 461), ("mid", 499),
             ("high", 661)])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_source_start_m331_sentinel_rows")
        self.assertEqual(self.receipt["scale_modulus"], SCALE_MODULUS)
        self.assertEqual(self.receipt["attention_prime"], ATTENTION_PRIME)
        self.assertTrue(self.receipt["finite_sentinel_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["full_sweep_completed"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])

    def test_all_m331_sentinel_rows_pass(self):
        self.assertEqual(self.receipt["prime_row_count"], 4)
        self.assertEqual(self.receipt["component_row_count"], 12)
        self.assertEqual(self.receipt["degree5_total_row_count"], 4)
        self.assertEqual(self.receipt["dominance_row_count"], 16)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 16, "zero": 0, "negative": 0})

    def test_attention_prime_is_weakest_sentinel(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 331)
        self.assertEqual(weakest["prime_modulus"], ATTENTION_PRIME)
        self.assertEqual(weakest["label"], "00,12")
        self.assertTrue(self.receipt["weakest_prime_equals_attention_prime"])
        self.assertEqual(
            self.receipt["weakest_prime_distance_from_attention_prime"], 0)
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.9702648688514812)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.4702648688514812)

    def test_runtime_boundary_is_recorded(self):
        self.assertGreater(self.receipt["total_elapsed_seconds"], 100.0)
        self.assertIn("progress", self.receipt["full_sweep_runtime_blocker"])
        selected = self.receipt["scale_result"]["selected_primes"]
        self.assertEqual(
            [row["prime_modulus"] for row in selected],
            [331, 461, 499, 661])


if __name__ == "__main__":
    unittest.main()
