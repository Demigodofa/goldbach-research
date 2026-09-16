import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.json")


class MobiusMomentSquareDegree5Q46189SourceFactorPatternMapTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.comparison = cls.receipt["q38038_vs_q41990"]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_source_factor_pattern_map")
        self.assertTrue(
            self.receipt["finite_source_factor_pattern_map_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["source_block_interaction_sign_theorem_proved"])
        self.assertFalse(
            self.receipt["source_factor_isolation_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_simple_scalar_patterns_are_eliminated(self):
        patterns = self.receipt["patterns"]
        self.assertTrue(patterns["eliminate_plain_middle_loss_threshold"])
        self.assertTrue(
            patterns["eliminate_small_over_missing_product_monotonicity"])
        self.assertTrue(patterns["eliminate_missing_high_prime_alone"])
        self.assertIn("matrix", patterns["survives_as_candidate"])

    def test_q38038_and_q41990_cross_block_signs_split(self):
        q38038 = self.comparison["q38038"]
        q41990 = self.comparison["q41990"]
        self.assertAlmostEqual(
            q38038["aggregate_non_middle_sum"],
            0.09269980585259228,
            places=15,
        )
        self.assertAlmostEqual(
            q41990["aggregate_non_middle_sum"],
            -0.10078449680431602,
            places=15,
        )
        self.assertGreater(
            self.comparison[
                "q38038_first_two_block_interaction"]["non_middle_sum"],
            0,
        )
        self.assertLess(
            self.comparison[
                "q41990_first_two_block_interaction"]["non_middle_sum"],
            0,
        )

    def test_next_action_is_all_row_block_sign_audit(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(action["name"],
                         "source-block interaction sign invariant")
        self.assertIn("all 34", action["smallest_next_test"])
        self.assertIn("input-side", action["falsifier"])


if __name__ == "__main__":
    unittest.main()
