import json
import unittest
from pathlib import Path


class Q286ResidualCharacterTriangleBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-character-triangle-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_full_character_triangle_route_too_broad")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["character_sum_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("too broad", receipt["decision"])

    def test_character_expansion_is_broad_but_exact(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["selected_target_count"], 7)
        self.assertEqual(summary["actual_full_positive_count"], 5)
        self.assertEqual(summary["triangle_certified_positive_count"], 4)
        self.assertGreaterEqual(
            summary["active_character_count_summary"]["minimum"], 2850)
        self.assertLess(
            summary["maximum_character_reconstruction_error"], 1e-12)

    def test_tight_row_requires_tiny_uniform_character_budget(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["tightest_positive_uniform_budget_row"]

        self.assertEqual(tight["target"], 94856)
        self.assertEqual(tight["active_character_count"], 2879)
        self.assertAlmostEqual(
            tight["uniform_per_character_discrepancy_budget"],
            0.003300082253073864)
        self.assertAlmostEqual(
            tight["max_actual_character_discrepancy"],
            0.12748865801232862)
        self.assertGreater(
            tight["max_actual_to_uniform_budget_ratio"], 38.0)
        self.assertGreater(
            tight["triangle_bound_to_aligned_margin_ratio"], 12.0)
        self.assertFalse(tight["triangle_bound_certifies_row"])

    def test_later_easy_rows_are_triangle_certified_only(self):
        receipt = self.load_receipt()
        certified = [
            row["target"] for row in receipt["target_rows"]
            if row["actual_full_positive"] and row["triangle_bound_certifies_row"]
        ]

        self.assertEqual(certified, [1222142, 1240888, 1242118, 1379072])


if __name__ == "__main__":
    unittest.main()
