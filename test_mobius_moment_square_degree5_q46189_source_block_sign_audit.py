import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-source-block-sign-audit.json")


class MobiusMomentSquareDegree5Q46189SourceBlockSignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"], "AUDIT_q46189_source_block_sign")
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["source_block_interaction_sign_theorem_proved"])
        self.assertFalse(
            self.receipt["source_factor_isolation_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_all_row_shape_falsifies_uniform_3x3_premise(self):
        self.assertEqual(self.receipt["row_count"], 34)
        self.assertEqual(
            self.receipt["source_block_count_distribution"],
            {"3": 32, "5": 2},
        )
        self.assertEqual(
            sorted(self.receipt["non_three_block_rows"]),
            [17290, 22610],
        )
        self.assertFalse(
            self.receipt["classification"][
                "all_rows_have_3x3_source_block_matrix"])

    def test_first_off_diagonal_signs_are_mixed(self):
        counts = self.receipt["first_off_diagonal_sign_counts"]
        self.assertEqual(counts["positive"], 20)
        self.assertEqual(counts["negative"], 14)
        self.assertEqual(counts["zero"], 0)
        self.assertEqual(counts["missing"], 0)

    def test_curvature_baseline_remains_falsified(self):
        curvature = self.receipt["curvature_baseline"]
        self.assertEqual(curvature["valid_row_count"], 32)
        self.assertEqual(curvature["match_count"], 13)
        self.assertEqual(curvature["mismatch_count"], 19)
        self.assertTrue(
            self.receipt["classification"][
                "source_gap_curvature_universal_sign_rule_falsified"])

    def test_best_single_feature_rule_is_not_theorem_level(self):
        best = self.receipt["best_rule"]
        self.assertGreater(best["mismatch_count"], 0)
        self.assertLess(best["match_count"], best["valid_row_count"])
        self.assertFalse(
            self.receipt["classification"][
                "single_feature_input_side_sign_rule_established"])
        self.assertIn("variable-size source-block matrix",
                      self.receipt["candidate_next_action"]["name"])


if __name__ == "__main__":
    unittest.main()
